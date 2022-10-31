from flask import Flask, jsonify, request
from logging import Logger
from src.url_analyser import URLAnalyser


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
