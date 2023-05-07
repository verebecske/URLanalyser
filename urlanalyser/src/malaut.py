import requests
import os
from selenium import webdriver
from src.ancestor import Ancestor
from py7zr import SevenZipFile

class Malaut(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def create_screenshot(self, url: str, path: str) -> None:
        resp = requests.get(url)
        try:
            self.call_selenium(url, path)
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

    def call_selenium(self, url: str, path: str):
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            options=firefox_options,
        )
        driver.get(url)
        driver.save_screenshot(path)
        driver.quit()

    def collect_data(self, url: str):
        pass

    def create_7z_file(self):
        original_file_path = ""
        compressed_file_path = ""
        password = self.generate_password()
        with SevenZipFile(compressed_file_path, 'w', password=password) as arc:
            arc.writeall(original_file_path)
        return compressed_file_path, password
