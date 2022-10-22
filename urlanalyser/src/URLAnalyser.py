from logging import Logger
import random
import re


class URLAnalyser:
    logger: Logger

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.logger.info("Start URLAnalyser")

    def is_malware(self, url: str) -> bool:
        self.logger.info("Start")
        return self.is_malware(url) == "ok"

    def dummy_is_malware(self, url: str) -> bool:
        self.logger.info("Start")
        return random.randint(0, 100) < 70

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None
