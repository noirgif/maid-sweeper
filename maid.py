import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
import sys
import tracemalloc
from typing import Awaitable, Callable, ParamSpec, TypeVar
import fire
import motor.motor_asyncio
import nest_asyncio
from pymongo import ASCENDING
from common.context import Context
from dispatchers.directory import Directory
from dispatchers.exec import Exec

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
        )
        self.debug = debug_mode

    def _debug_async(self, func: Callable[P, Awaitable[R]], *args: P.args, **kwargs: P.kwargs) -> Awaitable[R]:
        """
        Run an async command with debug mode if specified. """
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

        if self.debug:
            async def _inner(x: Awaitable[R]) -> R:
                res = await x
                tracemalloc.stop()
                return res
        
            result = _inner(result)

        return result


    async def _sweep(self, keywords: list[str], args: tuple[str]):
        exec_dispatch = Exec()
        cursor = self.context.db.file_metadata.find(
            {"tags": {'$in': keywords}})
        async for document in cursor:
            path = Path(document['path'])
            await self.context.dispatch(exec_dispatch, path, args)

    async def _tag(self, path: Path):
        await self.context.dispatch(Directory(), path)
        self.context.db.file_metadata.create_index([("tags", ASCENDING)])

    def sweep(self, keywords: list[str], *exec_args: str):
        """Sweep the database for files with the given keywords and run the given function on them.
        Args:
            keywords: The keywords to search for.
            func: The function to run on the files.
        """
        print(f"keywords: {keywords}, exec_args: {exec_args}")
        coro = self._debug_async(self._sweep, keywords, exec_args)
        self.context.loop.run_until_complete(coro)

    def tag(self, path: str):
        """Tag a file or directory.

        Args:
            path: The path to the file or directory to tag.
        """
        coro = self._debug_async(self._tag, Path(path))
        self.context.loop.run_until_complete(coro)


if __name__ == "__main__":
    fire.Fire(MaidSweeper)
