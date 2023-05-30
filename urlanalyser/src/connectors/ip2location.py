from src.ancestor import Ancestor
import re
import socket
import requests


class IP2LocationAPI(Ancestor):
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
        api_key = self.config["ip2location_api_key"]
        response = requests.get(
            f"https://api.ip2location.io/?key={api_key}&ip={ip_addr}"
        )
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def format_answer(self, response: dict) -> dict:
        return {
            "country code": response["country_code"],
            "country": response["country_name"],
            "city": response["city_name"],
        }

    # ez igazabol a domage-t tudja kivaltani, szoval javítsuk ki
    def get_domain_whois(self, url):
        api_key = self.config["ip2location_api_key"]
        response = requests.get(
            f"https://api.ip2whois.com/v2?key={api_key}&domain={domain}"
        )
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}
