from logging import Logger
import random
from src.ancestor import Ancestor


class APIConnector(Ancestor):
    logger: Logger
    config: dict

    def logs(func):
        def wrapper(self, *args, **kwargs):
            self.logger.error(f"Start {func.__name__}")
            ret = func(self, *args, **kwargs)
            self.logger.error(f"Stop {func.__name__}")
            return ret

        return wrapper

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.config = config

    @logs
    def send_request_to_virustotal(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            with open("datas/virustotal_ans.json", "r") as file:
                return json.load(file)["last_analysis_stats"]
        return "error"

    @logs
    def send_request_to_urlhaus(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            with open("datas/urlhaus_ans.json", "r") as file:
                return json.load(file)["query_status"]
        return "error"

    def get_ip(self, url: str) -> str:
        return "127.0.0.1"

    @logs
    def get_geoip(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            return ["Sweden"]
        return "error"
