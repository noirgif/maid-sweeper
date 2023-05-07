import asyncio
from pathlib import Path
from maid_sweeper.common.context import Context
from maid_sweeper.common.interface import Dispatcher
from maid_sweeper.common.patterns import TYPICAL_FILES_RE
from maid_sweeper.dispatchers.file import File
from maid_sweeper.dispatchers.tag import Tag

class Directory(Dispatcher):
    async def dispatch(self, context: Context, directory: Path):
        for path in directory.iterdir():
            for directory_type in TYPICAL_FILES_RE:
                    if TYPICAL_FILES_RE[directory_type].match(path.name):
                        await context.dispatch(Tag(self), directory, [directory_type])
                        # do not continue if the whole directory is tagged
                        return
                        # TODO: further categorize the directory
                        # by reading its {"tag": "document"} files
                        # should be able to be toggled

        tasks = []        
        for path in directory.iterdir():
            task_file = asyncio.create_task(context.dispatch(File(self), path))
            tasks.append(task_file)
            if path.is_dir():
                task_dir = asyncio.create_task(context.dispatch(Directory(self), path))
                tasks.append(task_dir)
        await asyncio.gather(*tasks)

        # TODO: group similarly named files together
        # TODO: group .exe with "misc" files, if there are many, as it indicates a software