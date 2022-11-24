import requests
import os
from selenium import webdriver
from logging import Logger
from src.ancestor import Ancestor


class Malaut(Ancestor):
    def __init__(self, config: dict):
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

    def create_screenshot(self, url: str) -> str:
        filename = "screenshot.png"
        path = "./src/flask/static/" + filename
        os.system(
            f"chromium-browser --no-sandbox --headless --screenshot='{path}' {url}"
        )
        # --window-size=411,2000
        return filename

    def get_screenshot(self, url: str):
        path = self.create_screenshot(url)
        try:
            return send_from_directory("/src/flask/static/", path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": "Not valid url"}), 404

    def get_repath(self):
        path_list = []
        url = request.args.get("url", default="", type=str)
        if not url.startswith("http"):
            url = "http://" + url
        is_next = True
        while is_next:
            resp = requests.get(url)
            if is_next:
                is_next = False
                print(resp.history)
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
        return jsonify({"path": path_list})
