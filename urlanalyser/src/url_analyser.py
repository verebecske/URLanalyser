from logging import Logger
import random
import re
from src.api_connector import APIConnector
from src.ancestor import Ancestor


class URLAnalyser(Ancestor):
    logger: Logger
    debug: bool = True
    connector: APIConnector

    def logs(func):
        def wrapper(self, *args, **kwargs):
            self.logger.error(f"Start {func.__name__}")
            ret = func(self, *args, **kwargs)
            self.logger.error(f"Stop {func.__name__}")
            return ret

        return wrapper

    def __init__(self, config: dict, logger: Logger, connector: APIConnector):
        self.logger = logger
        self.debug = bool(config["debug"])

    @logs
    def is_malware(self, url: str) -> bool:
        if self.debug:
            return self.dummy_is_malware(url)
        raise ValueError("not yet :(")

    def dummy_is_malware(self, url: str) -> bool:
        return random.randint(0, 100) < 70

    @logs
    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None
