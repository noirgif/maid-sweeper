import asyncio
from pathlib import Path
import shlex
from common.context import Context
from common.types import Dispatcher


class Exec(Dispatcher):
    async def dispatch(self, context: Context, path: Path, args: list[str]):
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

        # run command
        await asyncio.create_subprocess_shell(shlex.join(new_args))
