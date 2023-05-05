from typing import Type
from common.context import Context
from common.types import Dispatcher


_dispatchers = {}
_dispatchers_options = {}

def register_dispatcher(dispatcher: Type[Dispatcher], name: str, *args, **options):
    """Register a dispatcher with the given name.

    Args:
        name (str): The name of the dispatcher.
        dispatcher (Dispatcher): The dispatcher to register.
        args: The arguments to pass to the dispatcher. For example, args = ['db'] means that the dispatcher will be initialized as dispatcher(db).
        options: The options to pass to the dispatcher.
    """
    if name in _dispatchers:
        raise ValueError("Dispatcher with name {} already registered".format(name))
    _dispatchers[name] = dispatcher
    options['args'] = args
    _dispatchers_options[name] = options


def get_dispatcher(name, context: Context) -> Type[Dispatcher]:
    """Get the dispatcher with the given name.

    Args:
        name (str): The name of the dispatcher.
        context (Context): The context to pass to the dispatcher. It includes the database.

    Returns:
        Dispatcher: The dispatcher with the given name.
    """
    if name not in _dispatchers:
        raise ValueError("Dispatcher with name {} not registered".format(name))
    
    options = _dispatchers_options[name]

    call_args = []
    for arg in options['args']:
        if arg == 'db':
            call_args.append(context.db)
        else:
            raise ValueError("Unknown argument {} for dispatcher {}".format(arg, name))
    
    return _dispatchers[name](*call_args, **options)
    