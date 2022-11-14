from logging import Logger, getLogger
import types
import functools


class LoggerMeta(type):
    logger: Logger

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
        logger = getLogger()
        return logger


class Ancestor(metaclass=LoggerMeta):
    config: dict
    debug: bool = True

    def working(self):
        print("Hey")

    def working2(self, msg):
        print(f"ti: {msg}")

    def __init__(self, config: dict):
        self.config = config


class Child(Ancestor):
    def working(self):
        print("Hey ti")

