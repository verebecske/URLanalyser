import requests
import socket
import re
import base64
from src.ancestor import Ancestor


class APIConnector(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request_to_virustotal(self, url: str) -> dict:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_key = self.config["virustotal_api_key"]
        headers = {"accept": "application/json", "x-apikey": api_key}
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers
        )
        if response.status_code == 200:
            return response.json()["data"]["attributes"]["last_analysis_stats"]
        else:
            return {"error": response.text}

    def send_request_to_urlhaus(self, url: str) -> dict:
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            query_status = response.json()["query_status"]
            ans = {"query_status": query_status}
            if query_status == "ok":
                ans["threat"] = response.json()["threat"]
                ans["url_status"] = response.json()["url_status"]
            return ans
        else:
            return {"error": response.text}

    def get_ip(self, url: str) -> str:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+"
        domain = re.match(pattern, url)[0]
        if "http" in domain:
            domain = domain.split("//")[1]
        ip_addr = socket.gethostbyname(domain)
        return ip_addr

    def get_geoip(self, url: str) -> dict:
        ip_addr = self.get_ip(url)
        response = requests.get(f"http://ipwho.is/{ip_addr}")
        if response.status_code == 200:
            ipwhois = response.json()
            return ipwhois["country"]
        else:
            return {"error": response.text}

    def create_screenshot(self, url: str) -> str:
        filename = "screenshot.png"
        path = "./src/flask/static/" + filename
        url = self.create_valid_url(url)
        resp = requests.get(url)
        os.system(
            f"chromium-browser --no-sandbox --headless --screenshot='{path}' {resp.url}"
        )
        # --window-size=41