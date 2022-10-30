from logging import Logger
import requests
import socket
import re
import base64


class APIConnector:
    logger: Logger
    config: {}

    def __init__(self, config: dict, logger: Logger):
        self.logger = logger
        self.logger.info("Start URLAnalyser")
        self.config = config

    def send_request_to_virustotal(self, url: str) -> str:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_key = self.config["virustotal_api_key"]
        headers = {"accept": "application/json", "x-apikey": api_key}
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return "error"

    def send_request_to_urlhause(self, url: str) -> str:
        if not self.valid_url(url):
            return "not valid url"
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            return response.json()["query_status"]
        else:
            return "error"

    def get_ip(self, url: str) -> str:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+"
        domain = re.match(pattern, url)[0]
        if "http" in domain:
            domain = domain.split("//")[1]
        ip_addr = socket.gethostbyname(domain)
        return ip_addr

    def get_geoip(self, url: str) -> str:
        ip_addr = self.get_ip(url)
        response = requests.get(f"http://ipwho.is/{ip_addr}")
        if response.status_code == 200:
            ipwhois = response.json()
            return ipwhois["country"]
        else: 
            return "error"
