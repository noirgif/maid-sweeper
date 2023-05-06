import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
import sys
import warnings
import motor.motor_asyncio
from common.context import Context
from dispatchers.directory import Directory
import nest_asyncio

# logging.basicConfig(level=logging.DEBUG)
# if not sys.warnoptions:
#     import os, warnings
#     warnings.simplefilter("default") # Change the filter in this process
#     os.environ["PYTHONWARNINGS"] = "default" # Also affect subprocesses]

nest_asyncio.apply()


if __name__ == "__main__":
    db = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')['sweep_maid']
    loop = asyncio.get_event_loop()
    context = Context(
       db=db,
       loop=loop,
       executor=ThreadPoolExecutor(max_workers=12), 
    )

    # classify a directory
    loop.run_until_complete(context.dispatch(Directory(), Path(r"F:\Game")))