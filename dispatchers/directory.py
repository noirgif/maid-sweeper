import asyncio
from pathlib import Path
import re
from common.context import Context
from common.types import Dispatcher
from common.patterns import TYPICAL_FILES
from dispatchers.file import File
from dispatchers.tag import Tag

class Directory(Dispatcher):
    async def dispatch(self, context: Context, directory: Path):
        for path in directory.iterdir():
            for directory_type in TYPICAL_FILES:
                for regex in TYPICAL_FILES[directory_type]:
                    if re.match(regex, path.name, re.IGNORECASE):
                        await context.dispatch(Tag(self), directory, [directory_type])
                        return
                        # do not continue if the whole directory is tagged
                        # TODO: further categorize the directory
        for path in directory.iterdir():
            task_file = asyncio.create_task(context.dispatch(File(self), path))
            if path.is_dir():
                task_dir = asyncio.create_task(context.dispatch_threads(Directory(self), path))
                await asyncio.gather(task_file, task_dir)
            else:
                await task_file

        # TODO: group similar files together