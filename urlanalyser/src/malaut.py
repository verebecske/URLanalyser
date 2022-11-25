import requests
import os
from selenium import webdriver
from logging import Logger
from src.ancestor import Ancestor


class Malaut(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config

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
