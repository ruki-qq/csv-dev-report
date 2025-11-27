import inspect
import logging
from functools import wraps
from pathlib import Path
from typing import Callable, Optional


def setup_logging(
    level: int = logging.DEBUG,
    log_to_file: bool = True,
    log_to_console: bool = False,
    log_dir: str = "logs",
) -> None:
    """
    Configuring logging for the application.

    Args:
        level: Logging level (default: DEBUG).
        log_to_file: Whether to log to file (default: True).
        log_to_console: Whether to log to console (default: False).
        log_dir: Directory for log files (default: "logs").
    """

    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    formatter = logging.Formatter(
        fmt="[%(asctime)s.%(msecs)03d] %(levelname)-7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers = []

    if log_to_file:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_path / f"app_{timestamp}.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Getting a logger instance for the given module name.

    Args:
        name: Module name (usually __name__).

    Returns:
        Logger instance.
    """

    return logging.getLogger(name)


def _get_function_info(func: Callable) -> tuple[str, int]:
    """
    Extract function location information.

    Args:
        func: Function to extract info from.

    Returns:
        Tuple of (module_name, line_number).
    """

    func_module = func.__module__.split(".")[-1]

    try:
        func_line = inspect.getsourcelines(func)[1]
    except (OSError, TypeError):
        func_line = 0

    return func_module, func_line


def _get_doc_first_line(func: Callable) -> str:
    """
    Extract first non-empty line from function docstring.

    Args:
        func: Function to extract docstring from.

    Returns:
        First line of docstring or function name.
    """

    docstring = func.__doc__

    if not docstring:
        return func.__name__

    lines = docstring.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped:
            return stripped

    return func.__name__


def _create_wrapper(
    func: Callable, logger: logging.Logger, func_module: str, func_line: int
) -> Callable:
    """
    Creating wrapper function for logging.

    Args:
        func: Function to wrap.
        logger: Logger instance to use.
        func_module: Module name.
        func_line: Line number.

    Returns:
        Wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        doc_first_line = _get_doc_first_line(func)
        func_identifier = f"{func_module}:{func_line} {func.__qualname__}"

        logger.debug(f"[{func_identifier}] Start {doc_first_line}")
        logger.debug(f"[{func_identifier}] args={args}, kwargs={kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.debug(f"[{func_identifier}] Completed successfully")
            return result
        except Exception as e:
            logger.exception(f"[{func_identifier}] Exception raised: {str(e)}")
            raise

    return wrapper


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
        func_module, func_line = _get_function_info(func)
        nonlocal logger

        if logger is None:
            logger = get_logger(func.__module__)

        return _create_wrapper(func, logger, func_module, func_line)

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)
