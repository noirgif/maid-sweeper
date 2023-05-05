from pathlib import Path
from common.types import Dispatcher, Signal

@Dispatcher.register("directory")
class Directory(Dispatcher):
    def __init__(self, directory: Path):
        self.directory = directory
        self.handlers = {
            "stop": self.stop
        }

    def dispatch(self):
        for inode in self.directory.iterdir():
            if inode.is_dir():
                yield ('directory', self.directory)
            else:
                yield ('file', inode)
    
    def stop(self, path: Path):
        # Stop the current directory
        if path == self.directory:
            yield Signal("directory.stop")