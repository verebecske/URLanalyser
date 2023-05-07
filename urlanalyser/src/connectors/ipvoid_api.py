from src.ancestor import Ancestor
import re
import socket
import requests


class IPVoidAPI(Ancestor):
    config: dict

# IP-t ker
# ThreatLog.com -ot meg integrald
# URL Reputation!!!

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request(self, url: str) -> dict:
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def get_is_malicous_result(self, url) -> bool:
        result = self.send_request(url)
        try:
            match response["query_status"]:
                case "invalid_url": return False
                case "no_result": return False
                case "ok": return True
        except: 
            pass
        return True    

    def format_answer(self, response: dict) -> dict:
        return response["country"]

    def get_url_reputation(self, url):
        endpoint = f"https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key={self.api_key}&url={url}"