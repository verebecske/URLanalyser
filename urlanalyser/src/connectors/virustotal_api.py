from src.ancestor import Ancestor
import base64
import requests
import re


class VirusTotalAPI(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request(self, url: str) -> dict:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_key = self.config["virustotal_api_key"]
        headers = {"accept": "application/json", "x-apikey": api_key}
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers
        )
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def format_answer(self, response: dict) -> dict:
        return response["data"]["attributes"]["last_analysis_stats"]
