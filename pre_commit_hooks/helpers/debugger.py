import sys
from collections.abc import Generator
from contextlib import contextmanager


# https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode
def is_debugger_active() -> bool:
    """Return if debugger is active."""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None


@contextmanager
def input_as_args() -> Generator[None, None, None]:
    """Context manager modifying `sys.argv` to pass CLI arguments via input while using debugger."""
    if is_debugger_active():
        args = input("Arguments: ")
        if args:
            sys.argv.extend(args.split(" "))

    yield
