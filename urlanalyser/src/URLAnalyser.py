from loguru import logger
import random
import requests


class URLAnalyser:
    logger: logger

    def __init__(self, config: dict, logger: logger):
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


if __name__ == "__main__":
    safeurl = URLAnalyser({}, logger=logger)
    # url = "https://urlhaus-api.abuse.ch/"
    url = "http://113.88.209.132:42715/i"
    ans = safeurl.dummy_is_malware(url)
    print(ans)
