from pathlib import Path
import pymongo
from common.types import Dispatcher

@Dispatcher.register("tag", "dict")
class Tag(Dispatcher):
    def __init__(self, db: dict[str, list]):
        self.db = db
    
    def dispatch(self, path: Path, tags: list[str]):
        self.db["file_metadata"].append({
            "path": str(path),
            "tags": tags
        })