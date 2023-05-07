from pathlib import Path
from maid_sweeper.common.context import Context
from maid_sweeper.common.interface import Dispatcher

class Tag(Dispatcher):
    async def dispatch(self, context: Context, path: Path, tags: list[str]):
        context.db.file_metadata.insert_one({
            "path": str(path),
            "tags": tags
        })