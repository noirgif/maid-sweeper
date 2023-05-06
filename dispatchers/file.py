from pathlib import Path
import re
from common.context import Context
from common.patterns import EXTENSIONS, FILENAME_PATTERNS
from common.types import Dispatcher
from dispatchers.tag import Tag



class File(Dispatcher):
    async def dispatch(self, context: Context, path: Path):
        # match types based on extensions
        extension = path.suffix[1:]

        # extension-based tagging
        tags : list[str] = []
        for file_type in EXTENSIONS:
            if extension in EXTENSIONS[file_type]:
                tags.append(file_type)
        
        # special cases 
        for file_tags, regex in FILENAME_PATTERNS:
            if re.match(regex, path.name):
                if type(file_tags) is str:
                    tags.append(file_tags)
                else:
                    tags += file_tags

        # TODO: more file name/date based tagging


        if tags:
            await context.dispatch(Tag(self), path, tags)
        elif path.is_file():
            # only tag files as misc
            await context.dispatch(Tag(self), path, ["misc"])

            # if it is misc, and not part of a software
            # try to read its name and content
            # if unintelligible, tag it as garbage