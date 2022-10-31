import requests
import os
from selenium import webdriver
from logging import Logger


class Malaut:
    def __init__(self, config: dict, logger: Logger):
        self.config = config

    def get_webpage(self, file):
        browser = webdriver.Firefox()
        browser.get("http://www.google.com/")
        browser.save_screenshot("screenie.png")

    def chrome(self):
        os.system("chrome --headless --disable-gpu --screenshot https://www.google.com")

    def start(self):
        malaut = Malaut()
        file = "test.html"
        # malaut.get_webpage(file)
