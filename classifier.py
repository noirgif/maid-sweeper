from pathlib import Path
from pymongo import MongoClient


class Classifier:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['file_archive']
        self.metadata_collection = self.db['file_metadata']

        self.curr_dir = []
    
    def __call__(self, path: Path) -> list[str]:
        # classify the file
        # return the tags
        # return [] if not found
        return self.classify(path)
    
    def classify(self, path: Path) -> list[str]:
        return []
    
    def into(self, path: Path):
        # notify the classifier when going into a directory
        pass
