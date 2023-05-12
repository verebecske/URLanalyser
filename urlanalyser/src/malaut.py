import requests
import os
import zipfile
import time
from selenium import webdriver
from src.ancestor import Ancestor


class Malaut(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.selenium_executor = "http://selenium-hub:4444/wd/hub"

    def create_screenshot(self, url: str, path: str) -> None:
        resp = requests.get(url)
        try:
            self.call_selenium(url, path)
            return
        except Exception as e:
            self.logger.error(str(e))
            raise e

    def get_redirection(self, url: str, all: bool = False) -> list:
        path_list = []
        resp = requests.get(url)
        data = {
            "status_code": resp.status_code,
            "url": resp.url,
            "redirect": resp.is_redirect,
            "redirection": [],
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
            data["redirection"].append(state)

        path_list.append(data)
        return path_list

    def collect(self, url):
        pass

    def call_selenium(self, url: str, path: str):
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor=self.selenium_executor,
            options=firefox_options,
        )
        driver.get(url)
        driver.save_screenshot(path)
        driver.quit()

    def create_zip_with_selenium(self, url: str, path: str):
        self.logger.info(f"Get url: {url}, get path: {path}")
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor=self.selenium_executor,
            options=firefox_options,
        )
        driver.get(url)
        time.sleep(3)
        source = driver.page_source
        with zipfile.ZipFile(path, mode="w") as archive:
            archive.writestr("/page.txt", source)
        driver.quit()
        self.logger.info(f"Created zip file")

    def collect_data(self, url: str):
        pass

    def delete_old_files(self):
        pass
