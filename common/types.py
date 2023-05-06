# Desc: Contains common types used throughout the project.

from abc import abstractmethod
import asyncio
from typing import TypeVar

Self = TypeVar("Self", bound="AbstractContext")

class AbstractContext:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def dispatch(self, dispatcher, *args, **kwargs):
        pass

    @abstractmethod
    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        pass

    @abstractmethod
    def clone_thread(self: Self, loop: asyncio.AbstractEventLoop) -> Self:
        pass


class Dispatcher:
    def __init__(self, parent=None):
        self.parent = parent

    @abstractmethod
    async def dispatch(self, context: AbstractContext, *args, **kwargs):
        """Handle a file, or further dispatch it to the appropriate child dispatcher."""
        pass

    def dispatch_thread(self, context: AbstractContext, *args, **kwargs):
        """Handle a file, or further dispatch it to the appropriate child dispatcher. But in a new thread."""
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.dispatch(context.clone_thread(loop), *args, **kwargs))
