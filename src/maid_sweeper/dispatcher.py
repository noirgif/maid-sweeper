from abc import abstractmethod
from typing import Any, Awaitable, Generic, ParamSpec, TypeVar
from maid_sweeper import patterns
from maid_sweeper.context import AsyncIOContext, ThreadAsyncIOContext, ThreadMotorContext
import asyncio
from pathlib import Path
from maid_sweeper.patterns import TYPICAL_FILES_RE

P = ParamSpec("P")
R = TypeVar('R')


class Dispatcher(Generic[P, R]):
    """An asynchronous dispatcher that handles a file. Use it when we do not want to use threads."""

    def __init__(self, parent=None):
        self.parent = parent

    @abstractmethod
    async def dispatch(self, context: AsyncIOContext, *args: P.args, **kwargs: P.kwargs) -> R:
        """Handle a file, or further dispatch it to the appropriate child dispatcher."""
        pass

    async def __call__(self, context: AsyncIOContext, *args: P.args, **kwargs: P.kwargs) -> R:
        return await self.dispatch(context, *args, **kwargs)


class ThreadDispatcher(Dispatcher[P, R]):
    """An asynchronous and multithreading dispatcher that handles a file."""

    def _new_thread_dispatch(self, context: ThreadAsyncIOContext, *args: P.args, **kwargs: P.kwargs) -> R:
        new_context = context.clone_thread()
        return asyncio.get_event_loop().run_until_complete(self.dispatch(new_context, *args, **kwargs))

    async def dispatch_thread(self, context: ThreadAsyncIOContext, *args: P.args, **kwargs: P.kwargs) -> R:
        """Handle a file in a new thread. Wait for it to finish."""
        return await asyncio.get_event_loop().run_in_executor(context.executor, self._new_thread_dispatch, context, *args, **kwargs)

    async def __call__(self, context: ThreadAsyncIOContext, *args: P.args, **kwargs: P.kwargs) -> R:
        return await self.dispatch_thread(context, *args, **kwargs)


class Exec(Dispatcher[[Path, list[str]], Any]):
    """A dispatcher that executes a command with the given path"""
    async def dispatch(self, context: AsyncIOContext, path: Path, args: list[str]):
        # replace arguments with path
        new_args: list[str] = []
        for arg in args:
            if arg == '{}':
                new_args.append(str(path))
            elif arg == '{/}':
                new_args.append(path.name)
            elif arg == '{//}':
                new_args.append(str(path.parent))
            elif arg == '{.}':
                new_args.append(str(path)[:-len(path.suffix)])
            elif arg == '{/.}':
                new_args.append(path.stem)
            elif arg == '{/.}':
                new_args.append(path.stem)
            else:
                new_args.append(arg)

        # run command
        if context.is_debug():
            print(f"Running command {new_args}")
        await asyncio.create_subprocess_exec(*new_args)


class Tag(Dispatcher[[Path, list[str]], Any]):
    """A dispatcher that tags a file with the given tags"""
    async def dispatch(self, context: ThreadMotorContext, path: Path, tags: list[str]):
        context.db.file_metadata.insert_one({
            "path": str(path),
            "tags": tags
        })


class File(ThreadDispatcher[[Path], Any]):
    """A dispatcher that handles a file. It may tag it or pass it to Exec."""
    async def dispatch(self, context: AsyncIOContext, path: Path):
        # match types based on extensions
        extension = path.suffix[1:]

        # extension-based tagging
        tags: list[str] = []
        for file_type in patterns.EXTENSIONS:
            if extension in patterns.EXTENSIONS[file_type]:
                tags.append(file_type)

        # special cases
        for file_tags, filename_pattern in patterns.FILENAMES_RE:
            if filename_pattern.match(path.name):
                if type(file_tags) is str:
                    tags.append(file_tags)
                else:
                    tags += file_tags

        # TODO: more file name/date based tagging

        # TODO: if it has no tag, and not part of a software
        # try to read its name and content
        # if unintelligible, tag it as garbage

        if tags:
            await Tag(self)(context, path, tags)
        elif path.is_file():
            # only tag files as misc
            await Tag(self)(context, path, ["misc"])


class Directory(ThreadDispatcher[[Path], Any]):
    """A dispatcher that handles a directory. It may tag it or pass it to File or Directory."""
    async def dispatch(self, context: ThreadAsyncIOContext, directory: Path):
        for path in directory.iterdir():
            for directory_type in TYPICAL_FILES_RE:
                if TYPICAL_FILES_RE[directory_type].match(path.name):
                    await Tag(self)(context, directory, [directory_type])
                    # do not continue if the whole directory is tagged
                    return
                    # TODO: further categorize the directory
                    # by reading its {"tag": "document"} files
                    # should be able to be toggled

        tasks = []
        for path in directory.iterdir():
            task_file = asyncio.create_task(File(self).__call__(context, path))
            tasks.append(task_file)
            if path.is_dir():
                task_dir = asyncio.create_task(
                    Directory(self)(context, path))
                tasks.append(task_dir)

        # TODO: group similarly named files together
        # TODO: group .exe with "misc" files, if there are many, as it indicates a software
        await asyncio.gather(*tasks)
