from pathlib import Path
import pymongo
from common.context import Context
from common.types import Dispatcher

class Tag(Dispatcher):
    def dispatch(self, context: Context, path: Path, tags: list[str]):
        context.db.file_metadata.insert_one({
            "path": str(path),
            "tags": tags
        })