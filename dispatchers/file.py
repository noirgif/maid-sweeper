from dispatchers import register_dispatcher
from common.types import Dispatcher

extension_tags = {
    "jpg": "image",
    "png": "image",
    "jpeg": "image",
    "mp4": "video",
    "mov": "video",
    "avi": "video",
    "mp3": "audio",
    "wav": "audio",
    "flac": "audio",
    "docx": "document",
    "pdf": "document",
    "txt": "document"
    
}

@register_dispatcher("file")
class File(Dispatcher):
    def __init__(self, path: str):
        self.path = path
    
    def dispatch(self):
        # match types based on extensions
        extension = self.path.split('.')[-1]

        actions = []
        if extension in extension_tags:
            actions.append(('tag', extension_tags[extension]))

        return actions 