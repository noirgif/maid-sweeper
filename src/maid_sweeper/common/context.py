from asyncio import AbstractEventLoop
import asyncio
from concurrent.futures import Executor
from typing import Callable, Self

from maid_sweeper.common.interface import AbstractContext, Dispatcher

class Context(AbstractContext):
    def __init__(self, db, loop: AbstractEventLoop, executor: Executor, debug=False):
        self.executor = executor
        self.loop = loop
        self.db = db
        self._debug = debug
    
    async def dispatch(self, dispatcher: Callable | Dispatcher, *args, **kwargs) -> None:
        """Sometimes we want to delegate it to another function to handle the file, we use dispatch for it"""
        if isinstance(dispatcher, Dispatcher):
            callable = dispatcher.dispatch
        else:
            callable = dispatcher
        # return self.loop.run_in_executor(self.executor, callable, self, *args, **kwargs)
        await callable(self, *args, **kwargs)
    
    async def dispatch_threads(self, dispatcher: Callable | Dispatcher, *args, **kwargs) -> None:
        """Sometimes we want to delegate it to another function to handle the file, we use dispatch for it"""
        if isinstance(dispatcher, Dispatcher):
            callable = dispatcher.dispatch_thread
        else:
            callable = dispatcher
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, callable, self, *args, **kwargs)
    
    def clone_thread(self, loop: asyncio.AbstractEventLoop) -> Self:
        """Clone the current thread's context into a new thread."""
        return Context(self.db, loop, self.executor, self._debug)

    def get_event_loop(self) -> AbstractEventLoop:
        return self.loop
    
    def is_debug(self) -> bool:
        return self._debug