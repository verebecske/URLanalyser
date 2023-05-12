from src.ancestor import Ancestor
import re
import socket
import requests


class IPWhoAPI(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def get_ip(self, url: str) -> str:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+"
        domain = re.match(pattern, url)[0]
        if "http" in domain:
            domain = domain.split("//")[1]
        ip_addr = socket.gethostbyname(domain)
        return ip_addr

    def get_location(self, url: str) -> dict:
        ip_addr = self.get_ip(url)
        response = requests.get(f"http://ipwho.is/{ip_addr}")
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def format_answer(self, response: dict) -> dict:
        return {
            "continent": response["continent"],
            "country": response["country"],
            "city": response["city"],
        }
