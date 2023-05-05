from pymongo import MongoClient
from common.context import Context

class Finder:
    def __init__(self, context: Context):
        self.metadata_collection = context.db['file_metadata']

    def find(self, keywords):
        # find the file based on keywords 
        # return the file path
        # return None if not found
        for entry in self.metadata_collection:
            if all([keyword in entry["tags"] for keyword in keywords]):
                yield entry['path']
