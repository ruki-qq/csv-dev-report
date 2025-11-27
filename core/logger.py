import inspect
import logging
from functools import wraps
from typing import Optional, Callable


def setup_logging(level: int = logging.DEBUG) -> None:
    """
    Configuring logging for the application.

    Args:
        level: Logging level (default: DEBUG)
    """

    logging.basicConfig(
        level=level,
        format="[%(asctime)s.%(msecs)03d] %(levelname)-7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_logger(name: str) -> logging.Logger:
    """
    Getting a logger instance for the given module name.

    Args:
        name: Module name (usually __name__)

    Returns:
        Logger instance
    """

    return logging.getLogger(name)


def log(_func: Optional[Callable] = None, *, logger: Optional[logging.Logger] = None):
    """
    Decorating function for logging purposes.

    Can be used with or without parameters:
        @log
        def func(): ...

        @log()
        def func(): ...

        @log(logger=custom_logger)
        def func(): ...

    Args:
        _func: Function to decorate
        logger: Optional logger instance (default: module logger)

    Returns:
        Decorated function
    """

    def decorator_log(func):
        func_file: str = inspect.getsourcefile(func) or "unknown"
        func_module: str = func.__module__.split(".")[-1]

        try:
            func_line: int = inspect.getsourcelines(func)[1]
        except (OSError, TypeError):
            func_line = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_logger(func.__module__)

            docstring: str | None = func.__doc__
            if docstring:
                doc_first_line: str = docstring.split("\n")[0].strip()
                if not doc_first_line:
                    doc_first_line = docstring.split("\n")[1].strip()
            else:
                doc_first_line: str = func.__name__

            func_identifier = f"{func_module}:{func_line} {func.__qualname__}"

            logger.debug(f"[{func_identifier}] Start {doc_first_line}")
            logger.debug(f"[{func_identifier}] args={args}, kwargs={kwargs}")

            try:
                result = func(*args, **kwargs)
                logger.debug(f"[{func_identifier}] Completed successfully")
                return result
            except Exception as e:
                logger.exception(f"[{func_identifier}] Exception raised: {str(e)}")
                raise e

        return wrapper

    if _func is None:
        # When called with parameters: @log() or @log(logger=...)
        return decorator_log
    else:
        return decorator_log(_func)
