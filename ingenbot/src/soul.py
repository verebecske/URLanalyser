import re
import requests
from abc import ABC, abstractmethod


class MaliciousContentError(Exception):
    def __str__(self):
        return "Woop-woop someone send something wrong!"


class Soul(ABC):
    debug = False

    @abstractmethod
    async def _send_message_to_log_channel(self, message):
        pass

    @abstractmethod
    async def _delete_message(self, message):
        pass

    @abstractmethod
    async def _send_answer(self, message, channel):
        pass

    @abstractmethod
    async def _send_file(self, image, channel):
        pass

    async def read_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")
        replay = ""
        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self.send_answer(replay, channel)
        url_list = self.filter_urls(req)
        if self.is_malicious_list(url_list):
            raise MaliciousContentError
        return replay

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        print("URLS:", urls)
        return urls

    def is_malicious_list(self, url_list: list) -> bool:
        is_malicious = False
        for url in url_list:
            is_malicious = is_malicious or self.inspect_url(url)
        print("Results:", is_malicious)
        return is_malicious

    def inspect_url(self, url: str) -> bool:
        mock_list = ["reallykaros.io", "virus.hu", "virus.com"]
        return url in mock_list

    async def read_direct_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")

        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self.send_answer(replay, channel)

        urls = self.filter_urls(req)
        if urls == []:
            replay = "Hey Tom, it's Bob!"
        else:
            replay = await self.send_to_analyser(urls, channel)
        return replay

    async def send_to_analyser(self, urls: list, channel) -> str:
        for url in urls:
            settings = {"urlhaus": True, "virustotal": True, "geoip": True}
            answer = self.ask_urlanalyser_api(url, settings)
            print("ANS:", answer)
            await self._send_answer(str(answer), channel)
            image = self.get_screenshot(url)
            await self._send_file(image, channel)
        return ""

    def encode_settings(self, settings: dict) -> str:
        res = [
            int(settings["urlhaus"]),
            int(settings["virustotal"]),
            int(settings["geoip"]),
        ]
        return "".join([str(i) for i in res])

    def ask_urlanalyser_api(self, url: str, settings: dict) -> dict:
        host = "urlanalyser-urlanalyser-1"
        port = 5000
        est = self.encode_settings(settings)
        r = requests.get(f"http://{host}:{port}/check?url={url}&sets={est}")
        if r.status_code == 200:
            return r.json()["result"]
        return {"result": ""}

    def get_screenshot(self, url: str) -> str:
        host = "urlanalyser-urlanalyser-1"
        port = 5000
        path = "./images/screenshot.png"
        r = requests.get(f"http://{host}:{port}/image?url={url}")
        with open(path, "wb") as image_file:
            image_file.write(r.content)
        return path
