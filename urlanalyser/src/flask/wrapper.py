from flask import Flask, jsonify, request
from logging import Logger
from src.url_analyser import URLAnalyser


class FlaskAppWrapper:
    logger: Logger
    analyser: URLAnalyser
    debug: bool

    def __init__(self, config: dict, analyser: URLAnalyser, logger: Logger):
        self.logger = logger
        self.analyser = analyser
        self.debug = bool(config["debug"])
        self.app = Flask(__name__)
        self.add_all_endpoints()

    def run(self) -> None:
        self.app.run(debug=self.debug)

    def add_all_endpoints(self):
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/check", "check", self.check)

    def index(self):
        data = {
            "message": f"Hey",
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
