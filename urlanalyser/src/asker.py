from logging import Logger
import random
import requests


class Asker:
    logger: Logger

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.logger.info("Start URLAnalyser")

    def send_request_to_virustotal(self, url: str) -> str:
        pass

    def send_request_to_urlhause(self, url: str) -> str:
        if not self.valid_url(url):
            return "not valid url"
        data = {"url": url}
        r = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if r.status_code == 200:
            print(r.json())
            return r.json()["query_status"]
        else:
            return "error"

    def get_geoip(self, url: str) -> str:
        pass

