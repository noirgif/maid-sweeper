from asyncio import AbstractEventLoop, Future
from concurrent.futures import Executor
from typing import Any, Callable
import typing

from common.types import AbstractContext, Dispatcher

T = typing.TypeVar("T")
class Context(AbstractContext):
    def __init__(self, db, loop: AbstractEventLoop, executor: Executor):
        self.executor = executor
        self.loop = loop
        self.db = db
    
    def dispatch(self, dispatcher: Callable[..., T | None] | Dispatcher, *args, **kwargs) -> None | T | Future[T | None]:
        if isinstance(dispatcher, Dispatcher):
            callable = dispatcher.dispatch
        else:
            callable = dispatcher
        return self.loop.run_in_executor(self.executor, callable, self, *args, **kwargs)
        # return callable(self, *args, **kwargs)
