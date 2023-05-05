from pathlib import Path
from pymongo import MongoClient
from classifier import Classifier
from concurrent.futures import ThreadPoolExecutor

from common.types import Action

class Sweeper:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['file_archive']

    def sweep(self, directory: Path, max_workers: int = 12) -> None:
        # sweep the directory and add them to the database
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            action = Action("directory", directory)
            action.run(executor)


