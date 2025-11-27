import logging
from functools import wraps


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configuring logging for the application.

    Args:
        level: Logging level (default: INFO)
    """

    logging.basicConfig(
        level=level,
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
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


def log(logger: logging.Logger = get_logger(__name__)):
    """
    Decorating function for logging purposes.

    Args:
        logger: Logger instance

    Returns:
        Decorated function
    """

    def decorator_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            doc_first_line = (
                func.__doc__.split("\n")[0].strip() if func.__doc__ else func.__name__
            )

            logging.info(f"Start {doc_first_line} with args: {args}, kwargs: {kwargs}")

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(f"Exception raised: {str(e)}")
                raise e

        return wrapper

    return decorator_log
