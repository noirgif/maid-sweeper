# Desc: Contains common types used throughout the project.

from abc import abstractmethod
from concurrent.futures import Executor
from pathlib import Path
from typing import Generator

from common.context import Context
import dispatchers


class Action:
    """Action is a generic action that can be run by an executor."""
    def __init__(self, dispatcher: str, *args, **kwargs):
        self.dispatcher = dispatcher
        self.args = args
        self.kwargs = kwargs

    def run(self, context: Context):
        dispatcher = dispatchers.get_dispatcher(self.dispatcher, context)
        return context.executor.submit(dispatcher.dispatch, *self.args, **self.kwargs)
    

class Signal(Action):
    """Signal is an action to be run by the parent dispatcher."""
    pass


class Dispatcher:
    @abstractmethod
    def dispatch(self, path: Path) -> Generator[Action | Signal, None, None]:
        """Handle a file, or further dispatch it to the appropriate child dispatcher."""
        pass

    @abstractmethod
    def handle(self, signal: Signal) -> Generator[Action | Signal, None, None]:
        """Handle a signal from a child dispatcher."""
        pass