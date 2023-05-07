from pathlib import Path
from maid_sweeper.common.context import Context
from maid_sweeper.common import patterns
from maid_sweeper.common.interface import Dispatcher
from maid_sweeper.dispatchers.tag import Tag



class File(Dispatcher):
    async def dispatch(self, context: Context, path: Path):
        # match types based on extensions
        extension = path.suffix[1:]

        # extension-based tagging
        tags : list[str] = []
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


        if tags:
            await context.dispatch(Tag(self), path, tags)
        elif path.is_file():
            # only tag files as misc
            await context.dispatch(Tag(self), path, ["misc"])

            # if it is misc, and not part of a software
            # try to read its name and content
            # if unintelligible, tag it as garbage