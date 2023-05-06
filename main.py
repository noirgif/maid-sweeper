import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from pathlib import Path
import sys
import warnings
import pymongo
from common.context import Context
from dispatchers.directory import Directory

loop = asyncio.new_event_loop()
loop.set_debug(True)
logging.basicConfig(level=logging.DEBUG)
if not sys.warnoptions:
    import os, warnings
    warnings.simplefilter("default") # Change the filter in this process
    os.environ["PYTHONWARNINGS"] = "default" # Also affect subprocesses]


if __name__ == "__main__":
    db = pymongo.MongoClient('mongodb://localhost:27017')['sweep_maid']

    context = Context(
       db=db,
       loop=loop,
       executor=ThreadPoolExecutor(max_workers=12), 
    )

    # classify a directory
    context.dispatch(Directory(), Path(r"F:\Game"))

    loop.run_until_complete(asyncio.sleep(1))
