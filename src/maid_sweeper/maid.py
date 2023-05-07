import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
import sys
import tracemalloc
from typing import Awaitable, Callable, ParamSpec, TypeVar
import motor.motor_asyncio
import nest_asyncio
from pymongo import ASCENDING
from maid_sweeper.common import patterns
from maid_sweeper.common.context import Context
from maid_sweeper.dispatchers.directory import Directory
from maid_sweeper.dispatchers.exec import Exec

P = ParamSpec("P")
R = TypeVar('R')


class MaidSweeper:
    def __init__(self, mongodb_url='mongodb://localhost:27017', database_name='sweep_maid', max_workers=24, debug_mode=False) -> None:
        nest_asyncio.apply()
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            mongodb_url)
        db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client[database_name]
        loop = asyncio.get_event_loop()
        self.context = Context(
            db=db,
            loop=loop,
            executor=ThreadPoolExecutor(max_workers=max_workers),
            debug=debug_mode
        )
        self.debug = debug_mode

    def _debug_async(self, func: Callable[P, Awaitable[R]], *args: P.args, **kwargs: P.kwargs) -> Awaitable[R]:
        """
        Run an async command with optional asyncio debugging"""
        if self.debug:
            tracemalloc.start()
            logging.basicConfig(level=logging.DEBUG)
            if not sys.warnoptions:
                import os
                import warnings
                # Change the filter in this process
                warnings.simplefilter("default")
                # Also affect subprocesses]
                os.environ["PYTHONWARNINGS"] = "default"
        result = func(*args, **kwargs)

        # stop tracemalloc after the result is realized
        if self.debug:
            async def _inner(x: Awaitable[R]) -> R:
                res = await x
                tracemalloc.stop()
                return res

            result = _inner(result)

        return result

    async def _sweep(self, keywords: tuple[str], args: tuple[str]):
        exec_dispatch = Exec()
        # replace synonyms with the actual keywords
        new_keywords = []
        for keyword in keywords:
            if keyword in patterns.SYNONYMS:
                new_keywords.extend(patterns.SYNONYMS[keyword])

        cursor = self.context.db.file_metadata.find(
            {"tags": {'$in': keywords}})
        async for document in cursor:
            path = Path(document['path'])
            await self.context.dispatch(exec_dispatch, path, args)

    async def _tag(self, path: Path):
        await self.context.dispatch(Directory(), path)
        self.context.db.file_metadata.create_index([("tags", ASCENDING)])

    def sweep(self, keywords: tuple[str], *exec_args: str):
        """Sweep the database for files with the given keywords and run the given function on them.
        Args:
            keywords: The comma separated list of keywords to specify the documents.
            exec_args: The command to run on the files. Use placeholders like {} as in find -exec or fd -x.
        """
        print(
            f"Running sweep with keywords {keywords} and command {exec_args}, sure? (y/n)")
        if input() != 'y':
            return
        coro = self._debug_async(self._sweep, keywords, exec_args)
        self.context.loop.run_until_complete(coro)

    def tag(self, path: str):
        """Tag a file or directory.

        Args:
            path: The path to the file or directory to tag.
        """
        coro = self._debug_async(self._tag, Path(path))
        self.context.loop.run_until_complete(coro)


def main():
    parser = argparse.ArgumentParser(description='Sweep maid')

    parser.add_argument('--mongodb-url', type=str, default='mongodb://localhost:27017',
                        help='The url to the mongodb instance to use.')
    parser.add_argument('--database-name', type=str,
                        default='sweep_maid', help='The name of the database to use.')
    parser.add_argument('--max-workers', type=int, default=24,
                        help='The maximum number of workers to use.')

    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode.')

    command_parser = parser.add_subparsers(
        dest='command', help='The command to run.')

    sweep_parser = command_parser.add_parser(
        'sweep', help='Sweep the database for files with the given keywords and run the given function on them.')
    sweep_parser.add_argument(
        'keywords', type=str, help='A comma separated list of keywords to specify the documents. E.g. `sweep game,video` passes `[\'game\',\'video\']` to the maid.')
    sweep_parser.add_argument('exec_args', type=str, nargs='+',
                              help='The command to run on the files. Use placeholders like {} as in find -exec or fd -x.')

    tag_parser = command_parser.add_parser(
        'tag', help='Tag a file or directory.')
    tag_parser.add_argument(
        'path', type=str, help='The path to the file or directory to tag.')

    args = parser.parse_args()

    maid = MaidSweeper(args.mongodb_url, args.database_name,
                       args.max_workers, args.debug)

    if args.command == 'sweep':
        maid.sweep(tuple(args.keywords.split(',')), *args.exec_args)
    elif args.command == 'tag':
        maid.tag(args.path)


if __name__ == '__main__':
    main()