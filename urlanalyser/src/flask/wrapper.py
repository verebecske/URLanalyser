import os
import datetime
from flask import Flask, jsonify, request, render_template, send_from_directory
from logging import Logger
import base64
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
        self.app.add_url_rule("/image", "get_screenshot", self.get_screenshot)

    def index(self):
        data = {
            "message": f"Hallo Welt",
            "status": 200,
        }
        return jsonify(data)

    def check(self):
        url = request.args.get("url", default="", type=str)
        sets = request.args.get("sets", default="111", type=str)
        status = 200
        if url == "":
            status = 400
            data = {
                "message": "Bad request!",
                "Error": "Unexpected error.",
            }
        else:
            result = self.analyser.collect_infos(url, sets)
            data = {
                "url": url,
                "result": result,
            }
        return jsonify(data), status

    def get_info(self):
        pass

    def create_screenshot(self, url: str) -> str:
        filename = "screenshot.png"
        path = "./src/flask/static/" + filename
        os.system(
            f"chromium-browser --no-sandbox --headless --screenshot='{path}' {url}"
        )
        # --window-size=411,2000
        return filename

    def get_screenshot(self):
        # url = "https://www.thetimenow.com/"
        url = request.args.get("url", default="", type=str)
        # if self.analyser.valid_url(url):
        path = self.create_screenshot(url)
        # path = "reigen.png"
        try:
            return send_from_directory("/src/flask/static/", path, as_attachment=True)
        except Exception as e:
            return str(e)
        # else:
        #     return jsonify({"error": "Not valid url"}), 404
