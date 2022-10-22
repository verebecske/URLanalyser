from logging import Logger
import random
import re
from src.api_connector import APIConnector


class URLAnalyser:
    logger: Logger
    debug: bool = True
    connector: APIConnector

    def logs(func):
        def wrapper(self, *args, **kwargs):
            self.logger.debug(f"Start {func.__name__}")
            return func(self, *args, **kwargs)
            self.logger.debug(f"Stop {func.__name__}")

        return wrapper

    def __init__(self, config: dict, connector: APIConnector, logger: Logger):
        self.logger = logger

    @logs
    def is_malware(self, url: str) -> bool:
        if self.debug:
            return self.dummy_is_malware(url)
        else:
            ValueError("not implemeneted. Yet!")

    def dummy_is_malware(self, url: str) -> bool:
        return random.randint(0, 100) < 70

    def valid_url(self, url: str) -> bool:
        self.logger.info("Start")
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None
