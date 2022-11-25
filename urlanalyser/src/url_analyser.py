import random
import re
import json
import os
import datetime
import requests
from src.api_connector import APIConnector
from src.ancestor import Ancestor
from src.malaut import Malaut


class URLAnalyser(Ancestor):
    connector: APIConnector

    def __init__(self, config: dict, connector: APIConnector, malaut: Malaut):
        super().__init__()
        self.connector = connector
        self.malaut = malaut

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
