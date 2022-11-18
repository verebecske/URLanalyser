from logging import Logger
import random
import re
import json
from src.api_connector import APIConnector
from src.ancestor import Ancestor


class URLAnalyser(Ancestor):
    logger: Logger
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
        self.connector = connector

    @logs
    def is_malware(self, url: str) -> bool:
        raise ValueError("not yet :(")

    @logs
    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None

    @logs
    def collect_infos(self, url: str, sets: str) -> dict:
        if self.valid_url(url):
            result = {}
            if sets[0] == "1":
                result["urlhaus"] = self.connector.send_request_to_urlhaus(url)
            if sets[1] == "1":
                result["virustotal"] = self.connector.send_request_to_virustotal(url)
            if sets[2] == "1":
                result["geoip"] = self.connector.get_geoip(url)
            return result
        return {"error": "error"}
