import os
import datetime
from flask import Flask, jsonify, request, render_template
from logging import Logger
from src.url_analyser import URLAnalyser
from src.malaut import Malaut
from splinter import Browser


class FlaskAppWrapper:
    logger: Logger
    analyser: URLAnalyser
    debug: bool
    config: dict

    def __init__(self, config: dict, logger: Logger, analyser: URLAnalyser):
        self.logger = logger
        self.analyser = analyser
        self.debug = bool(config["debug"])
        self.config = config
        self.app = Flask(__name__)
        self.add_all_endpoints()

    def run(self) -> None:
        host = self.config["host"]
        port = self.config["port"]
        self.app.run(debug=self.debug, host=host, port=port)

    def add_all_endpoints(self):
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/check", "check", self.check)
        self.app.add_url_rule("/test", "test_screenshot", self.test_screenshot)

    def index(self):
        data = {
            "message": f"Hallo Welt",
            "status": 200,
        }
        return jsonify(data)

    def check(self):
        url = request.args.get("url", default="", type=str)
        if url == "":
            data = {
                "message": "Bad request!",
                "status": 400,
                "Error": "Unexpected error.",
            }
        else:
            result = self.analyser.is_malware(url)
            data = {
                "message": f"Is {url} a malware? {result}",
                "status": 200,
                "result": result,
            }
        return jsonify(data)

    def test_screenshot(self):
        self.create_screenshot("https://www.thetimenow.com/")
        return render_template("image.html", date=datetime.datetime.now())

    def create_screenshot(self, url: str) -> str:
        path = "./src/flask/static/screenshot.png"
        os.system(
            f"chromium-browser --no-sandbox --headless --screenshot='{path}' {url}"
        )
        # --window-size=411,2000
        return path

    def test_splinter(self, url: str) -> str:
        browser = Browser("chrome", headless=True)
        browser.visit("https://www.thetimenow.com/")
        print("HEY")
        screenshot_path = browser.screenshot(
            "./src/flask/static/screenshot.png", full=True
        )
        return path

    def test_send_image(self):
        with open("yourfile.ext", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return {"image": encoded_string, "data": jsonify(return_list)}
