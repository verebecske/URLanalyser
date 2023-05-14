import logging
import functools


def get_logger():
    logging.basicConfig(
        format="-> %(asctime)s - %(filename)s - %(levelname)s - %(lineno)d - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    return logger


class LoggerMeta(type):
    logger: logging.Logger

    @staticmethod
    def _decorator(fun, logger):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            logger.debug(f"Start {fun.__name__} - {args} - {kwargs}")
            res = fun(*args, **kwargs)
            logger.debug(f"Stop {fun.__name__} - {args} - {kwargs}")
            return res

        return wrapper

    def __new__(self, name, bases, attrs):
        logger = get_logger()
        for key in attrs.keys():
            if callable(attrs[key]):
                fun = attrs[key]
                attrs[key] = LoggerMeta._decorator(fun, logger)
        return super().__new__(self, name, bases, attrs)


class Ancestor(metaclass=LoggerMeta):
    logger: logging.Logger

    def __init__(self):
        self.logger = get_logger()
