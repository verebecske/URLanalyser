import random
import re
import json
import os
import datetime
import requests
from src.api_connector import APIConnector
from src.ancestor import Ancestor


class URLAnalyser(Ancestor):
    connector: APIConnector

    def __init__(self, config: dict, connector: APIConnector):
        self.connector = connector

    def is_malware(self, url: str) -> bool:
        raise ValueError("not yet :(")

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None

    def collect_infos(self, url: str, sets: str) -> dict:
        if self.valid_url(url):
            result = {}
            if sets[0] == "1":
                result["urlhaus"] = self.connector.send_request_to_urlhaus(url)
            if sets[1] == "1":
                result["virustotal"] = self.connector.send_request_to_virustotal(url)
            if sets[2] == "1":
                result["geoip"] = self.connector.get_geoip(url)
            return result
        return {"error": "error"}

    def create_valid_url(self, url: str) -> str:
        if not valid_url(url):
            raise ValueError("not valid url")
        if not url.startswith("http"):
            url = "http://" + url
        return url

    def create_screenshot(self, url: str) -> str:
        filename = "screenshot.png"
        path = "./src/flask/static/" + filename
        url = self.create_valid_url(url)
        resp = requests.get(url)
        os.system(
            f"chromium-browser --no-sandbox --headless --screenshot='{path}' {resp.url}"
        )
        # --window-size=411,2000
        return filename

    def get_repath(self, url):
        path_list = []
        url = self.create_valid_url(url)
        resp = requests.get(url)
        data = {
            "status_code": resp.status_code,
            "url": resp.url,
            "cookies": str(resp.cookies),
            "redirect": resp.is_redirect,
            "headers": str(resp.headers),
            "history": [],
        }
        for h in resp.history:
            data["history"].append(
                {
                    "status_code": h.status_code,
                    "url": h.url,
                    "cookies": str(h.cookies),
                    "redirect": h.is_redirect,
                    "headers": str(h.headers),
                }
            )
        path_list.append(data)
        return path_list
