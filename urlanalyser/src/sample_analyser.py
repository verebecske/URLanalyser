import requests
import os
import zipfile
import time
import hashlib
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.ancestor import Ancestor


class SampleAnalyser(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        selenium_host = config.get("selenium_host", "selenium-hub")
        selenium_port = config.get("selenium_port", "4444")
        self.selenium_executor = f"http://{selenium_host}:{selenium_port}/wd/hub"

    def create_screenshot(self, url: str, path: str) -> None:
        resp = requests.get(url)
        try:
            self.call_selenium(url, path)
            return
        except Exception as error:
            self.logger.error(str(error))
            raise error

    def get_redirection(self, url: str, all: bool = False) -> list:
        path_list = []
        resp = requests.get(url)
        or_data = {
            "status_code": resp.status_code,
            "url": resp.url,
            "redirect": resp.is_redirect,
        }
        if all:
            or_data["headers"] = str(resp.headers)
            or_data["cookies"] = str(resp.cookies.items())
        for h in resp.history:
            data = {
                "status_code": h.status_code,
                "url": h.url,
                "redirect": h.is_redirect,
            }
            if all:
                data["cookies"] = str(h.cookies.items())
                data["headers"] = str(h.headers)
            path_list.append(data)
        path_list.append(or_data)
        return path_list

    def call_selenium(self, url: str, path: str):
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor=self.selenium_executor,
            options=firefox_options,
        )
        driver.set_window_size(1400, 1200)
        driver.get(url)
        driver.save_screenshot(path)
        driver.quit()

    def create_zip_with_selenium(self, url: str, path: str):
        self.logger.info(f"Get url: {url} - get path: {path}")
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor=self.selenium_executor,
            options=firefox_options,
        )
        driver.get(url)
        time.sleep(3)
        source = driver.page_source
        dots = url.split("/")
        page_name = (dots[-1]) if dots != [] else "source"
        with zipfile.ZipFile(path, mode="w") as archive:
            archive.writestr(f"/{page_name}", source)
        driver.quit()
        self.logger.info(f"Created zip file")

    def collect_malware_sample(self, url: str, path: str):
        self.logger.info(f"Get url: {url} - get path: {path}")
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor=self.selenium_executor,
            options=firefox_options,
        )
        driver.get(url)
        time.sleep(3)
        source = driver.page_source
        dots = url.split(".")
        extension = ("." + dots[-1]) if dots != [] else ""
        dots = url.split("/")
        page_name = (dots[-1]) if dots != [] else "source"
        encoded_source = source.encode()
        metadata = {
            "links": list(
                filter(
                    lambda a: a != "",
                    [
                        a.get_attribute("href")
                        for a in driver.find_elements(By.TAG_NAME, "a")
                    ],
                )
            ),
            "script": list(
                filter(
                    lambda a: a != "",
                    [s.text for s in driver.find_elements(By.TAG_NAME, "script")],
                )
            ),
            "extension": extension,
            "date": time.time(),
            "title": driver.title,
            "redirection": self.get_redirection(url, True),
            "hash": {
                "md5": hashlib.md5(encoded_source).hexdigest(),
                "sha1": hashlib.sha1(encoded_source).hexdigest(),
                "sha256": hashlib.sha256(encoded_source).hexdigest(),
            },
        }
        jmeta = json.dumps(metadata, indent=4)
        with zipfile.ZipFile(path, mode="w") as archive:
            archive.writestr(f"/{page_name}", source)
            archive.writestr(f"/metadata.json", jmeta)
        driver.quit()
        self.logger.info(f"Collected sample")
