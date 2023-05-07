import asyncio
from pathlib import Path
import re
import shlex
import sys
from maid_sweeper.common.context import Context
from maid_sweeper.common.interface import Dispatcher

def windows_quote(s):
    if not s:
        return '""'
    if re.search(r'[\s"\\]', s) is None:
        return s
    s = s.replace("\\", "\\\\").replace('"', '\\"') 
    return f'"{s}"'


class Exec(Dispatcher):
    async def dispatch(self, context: Context, path: Path, args: list[str]):
        if context.is_debug():
            print(f"Dispatching {path} to Exec {args}")
        # replace arguments with path
        new_args: list[str] = []
        for arg in args:
            if arg == '{}':
                new_args.append(str(path))
            elif arg == '{/}':
                new_args.append(path.name)
            elif arg == '{//}':
                new_args.append(str(path.parent))
            elif arg == '{.}':
                new_args.append(str(path)[:-len(path.suffix)])
            elif arg == '{/.}':
                new_args.append(path.stem)
            elif arg == '{/.}':
                new_args.append(path.stem)
            else:
                new_args.append(arg)
        
        command = ''
        # use windows quote if needed
        if sys.platform == 'win32':
            command = ' '.join([windows_quote(arg) for arg in new_args])
        else:
            command = shlex.join(new_args)
        
        # run command
        if context.is_debug():
            print(f"Running command {command}")
        await asyncio.create_subprocess_shell(command)
