from logging import Logger


class Ancestor:
    logger: Logger
    config: dict
    debug: bool = True

    def logs(func):
        def wrapper(self, *args, **kwargs):
            self.logger.error(f"Start {func.__name__}")
            ret = func(self, *args, **kwargs)
            self.logger.error(f"Stop {func.__name__}")
            return ret

        return wrapper

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.debug = bool(config["debug"])
