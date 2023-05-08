import argparse
import asyncio
import logging
import sys
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Awaitable, Callable, ParamSpec, TypeVar

import nest_asyncio
from pymongo import ASCENDING

from maid_sweeper import dispatcher, patterns
from maid_sweeper.context import ThreadMotorContext

P = ParamSpec("P")
R = TypeVar('R')


class MaidSweeper:
    def __init__(self, args: argparse.Namespace) -> None:
        nest_asyncio.apply()
        if args.debug:
            import os
            tracemalloc.start()
            logging.basicConfig(level=logging.DEBUG)
            os.environ["PYTHONASYNCIODEBUG"] = "1"
            if not sys.warnoptions:
                import warnings
                # Change the filter in this process
                warnings.simplefilter("default")
                # Also affect subprocesses
                os.environ["PYTHONWARNINGS"] = "default"

        self.context = ThreadMotorContext(
            executor=ThreadPoolExecutor(max_workers=args.max_workers),
            database_name=args.database_name,
            debug=args.debug,
            host=args.mongodb_host,
            port=args.mongodb_port,
        )

    def _debug_async(self, func: Callable[P, Awaitable[R]], *args: P.args, **kwargs: P.kwargs) -> Awaitable[R]:
        """Run an async command with optional asyncio debugging"""
        result = func(*args, **kwargs)
        # stop tracemalloc after the result is realized
        if self.context.is_debug():
            async def _inner(x: Awaitable[R]) -> R:
                res = await x
                tracemalloc.stop()
                return res

            result = _inner(result)

        return result

    async def _sweep(self, keywords: list[str], args: list[str]):
        exec_dispatch = dispatcher.Exec()
        # replace synonyms with the actual keywords
        new_keywords = []
        for keyword in keywords:
            if keyword in patterns.SYNONYMS:
                new_keywords.extend(patterns.SYNONYMS[keyword])

        cursor = self.context.db.file_metadata.find(
            {"tags": {'$in': new_keywords}})
        async for document in cursor:
            path = Path(document['path'])
            await exec_dispatch(self.context, path, args)

    async def _tag(self, paths: list[str]):
        tasks = []
        for path in paths:
            if self.context.is_debug():
                print(f"Tagging {path}")
            tasks.append(dispatcher.Directory().dispatch_thread(self.context, Path(path)))
        await asyncio.gather(*tasks)
        await self.context.db.file_metadata.create_index([("tags", ASCENDING)])

    def sweep(self, keywords: list[str], exec_args: list[str]):
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
        asyncio.get_event_loop().run_until_complete(coro)

    def tag(self, paths: list[str]):
        """Tag a file or directory.

        Args:
            path: The path to the file or directory to tag.
        """
        coro = self._debug_async(self._tag, paths)
        asyncio.get_event_loop().run_until_complete(coro)


def main():
    parser = argparse.ArgumentParser(description='Sweep maid')

    parser.add_argument('--mongodb-host', type=str, default='mongodb://localhost:27017',
                        help='The url to the mongodb instance to use.')
    parser.add_argument('--mongodb-port', type=int, default=27017,
                        help='The url to the mongodb instance to use.')
    parser.add_argument('--database-name', type=str,
                        default='sweep_maid', help='The name of the database to use.')
    parser.add_argument('--max-workers', type=int, default=24,
                        help='The maximum number of workers to use.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode.')

    command_parser = parser.add_subparsers(
        dest='command', help='The command to run.')

    tag_parser = command_parser.add_parser(
        'tag', help='Tag a file or directory.')
    tag_parser.add_argument(
        'paths', nargs='+', metavar='path', type=str, help='The root directories to tag.')

    sweep_parser = command_parser.add_parser(
        'sweep', help='Sweep the database for files with the given keywords and run the given function on them.')
    sweep_parser.add_argument(
        '-t', '--tag', type=str, nargs='*', action='extend', help='A list of tags to specify the documents. E.g. `sweep game,video` passes `[\'game\',\'video\']` to the maid.')

    sweep_parser.add_argument('-x', '--exec', type=str, nargs='+', dest='exec_args',
                              help='The command to run on the files. Use placeholders like {} as in find -exec or fd -x. Defaults to Danshari -- removing all of the files/directories  with the specified tags.')

    args = parser.parse_args()

    # set to Danshari mode if no exec args are given
    if sys.platform == 'win32':
        danshari = ['del', '/F', '/P', '{}']
    else:
        danshari = ['rm', '-r', '{}']
    if args.command == 'sweep' and args.exec_args is None:
        print(
            f"No exec args given, using default {danshari}. Sure? (yes/no)")
        if input() == 'yes':
            args.exec_args = danshari
        else:
            return

    maid = MaidSweeper(args)
    if args.command == 'sweep':
        maid.sweep(args.tag, args.exec_args)
    elif args.command == 'tag':
        maid = MaidSweeper(args)
        maid.tag(args.paths)


if __name__ == '__main__':
    main()
