# Desc: Contains common types used throughout the project.

from abc import abstractmethod


class AbstractContext:
    @abstractmethod
    def __init__(self):
        pass

class Dispatcher:
    def __init__(self, parent=None):
        self.parent = parent

    @abstractmethod
    def dispatch(self, context: AbstractContext, *args, **kwargs):
        """Handle a file, or further dispatch it to the appropriate child dispatcher."""
        pass