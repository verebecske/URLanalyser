import logging
import functools


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
        logger = self.get_logger()
        for key in attrs.keys():
            if callable(attrs[key]):
                fun = attrs[key]
                attrs[key] = LoggerMeta._decorator(fun, logger)
        return super().__new__(self, name, bases, attrs)

    def get_logger():
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)
        return logger


class Ancestor(metaclass=LoggerMeta):
    pass
