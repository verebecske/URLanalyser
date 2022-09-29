from logging import Logger
import random
import requests


class SafeURLApi:
    logger: Logger

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger

    def is_malware(self, url: str) -> bool:
        return self.is_malware(url) == "ok"

    def dummy_is_malware(self, url: str) -> bool:
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
    safeurl = SafeURLApi({}, None)
    # url = "https://urlhaus-api.abuse.ch/"
    url = "http://113.88.209.132:42715/i"
    ans = safeurl.send_request_to_urlhause(url)
    print(ans)
