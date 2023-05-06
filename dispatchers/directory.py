from pathlib import Path
import re
from common.context import Context
from common.types import Dispatcher
from common.patterns import TYPICAL_FILES
from dispatchers.file import File
from dispatchers.tag import Tag

class Directory(Dispatcher):
    def dispatch(self, context: Context, directory: Path):
        for path in directory.iterdir():
            for type in TYPICAL_FILES:
                for regex in TYPICAL_FILES[type]:
                    if re.match(regex, path.name, re.IGNORECASE):
                        context.dispatch(Tag(self), directory, [type])
                        # do not continue if the whole directory is tagged
                        # TODO: further categorize the directory
                        return
        for path in directory.iterdir():
            context.dispatch(File(self), path) # type: ignore
            if path.is_dir():
                context.dispatch(Directory(self), path) # type: ignore

        # TODO: group similar files together