from abc import abstractmethod
import asyncio
from concurrent.futures import ThreadPoolExecutor
import motor.motor_asyncio




class AbstractContext:
    @abstractmethod
    def __init__(self):
        pass


class AsyncIOContext(AbstractContext):
    def __init__(self, debug: bool):
        self._debug = debug

    def is_debug(self) -> bool:
        return self._debug


class ThreadAsyncIOContext(AsyncIOContext):
    def __init__(self, executor: ThreadPoolExecutor, debug: bool):
        super(ThreadAsyncIOContext, self).__init__(debug)
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
        self.executor = executor

    @abstractmethod
    def clone_thread(self) -> 'ThreadAsyncIOContext':
        """Clone the current thread's context into a new thread. Create new instances for non-thread-safe objects."""
        pass


class ThreadMotorContext(ThreadAsyncIOContext):
    DEFAULT_DBOPT = {
        'host': 'localhost',
        'port': 27017,
    }

    def __init__(self, executor: ThreadPoolExecutor, database_name='maid-sweep', debug=False, **dbopt):
        super(ThreadMotorContext, self).__init__(executor, debug)
        self.dbopt = ThreadMotorContext.DEFAULT_DBOPT | dbopt
        if self.dbopt['host'].startswith('mongodb+srv://') or ('ssl' in self.dbopt and self.dbopt['ssl']):
            import certifi
            ca = certifi.where()
            self.client = motor.motor_asyncio.AsyncIOMotorClient(**dbopt, tlsCAFile=ca)
        else:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(host=self.dbopt['host'], port=self.dbopt['port'])
        self.database_name = database_name
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client[
            database_name]

    def clone_thread(self) -> 'ThreadMotorContext':
        """Clone the current thread's context into a new thread."""
        return ThreadMotorContext(self.executor, self.database_name, self._debug, **self.dbopt)
