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

    def get_history(self, url: str, all: bool = False) -> list:
        path_list = []
        resp = requests.get(url)
        data = {
            "status_code": resp.status_code,
            "url": resp.url,
            "redirect": resp.is_redirect,
            "history": [],
        }
        if all:
            data["headers"] = str(resp.headers)
            data["cookies"] = str(resp.cookies)
        for h in resp.history:
            state = {
                "status_code": h.status_code,
                "url": h.url,
                "redirect": h.is_redirect,
            }
            if all:
                state["cookies"] = str(h.cookies)
                state["headers"] = str(h.headers)
            data["history"].append(state)

        path_list.append(data)
        return path_list

    def collect(self, url):
        pass
