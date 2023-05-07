from pathlib import Path
from common.context import Context
from common.types import Dispatcher

class Tag(Dispatcher):
    async def dispatch(self, context: Context, path: Path, tags: list[str]):
        context.db.file_metadata.insert_one({
            "path": str(path),
            "tags": tags
        })