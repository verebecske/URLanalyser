import requests
import os
from selenium import webdriver
from src.ancestor import Ancestor


class Malaut(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def create_screenshot(self, url: str, path: str) -> None:
        resp = requests.get(url)
        try:
            os.system(
                f"chromium-browser --no-sandbox --headless --screenshot='{path}' {resp.url}"
            )
            # --window-size=411,2000
            return
        except Exception as e:
            self.logger.error(str(e))
            raise e

    def get_history(self, url):
        path_list = []
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

    def collect(self, url):
        pass
