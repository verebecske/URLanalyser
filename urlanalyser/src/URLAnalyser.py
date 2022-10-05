import logging
import random
import requests
import re

class URLAnalyser:
    logger: logging.Logger

    def __init__(self, config: dict, logger: logging.Logger):
        self.logger = logger
        self.logger.info("Start URLAnalyser")

    def is_malware(self, url: str) -> bool:
        self.logger.info("Start")
        return self.is_malware(url) == "ok"

    def dummy_is_malware(self, url: str) -> bool:
        self.logger.info("Start")
        return random.randint(0, 100) < 70

    def send_request_to_urlhause(self, url: str) -> str:
        data = {"url": url}
        r = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if r.status_code == 200:
            print(r.json())
            return r.json()["query_status"]
        else:
            return "error"

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+$"
        res = re.match(pattern, url)
        return res != None

if __name__ == "__main__":
    logger = logging.getLogger()
    safeurl = URLAnalyser({}, logger=logger)
    url = "https://urlhaus-api.abuse.ch/"
    # url = "http://113.88.209.132:42715/i"
    ans = safeurl.dummy_is_malware(url)

