from flask import Flask, jsonify, request
from src.URLAnalyser import URLAnalyser
from logging import Logger


class FlaskAppWrapper(object):
    logger: Logger

    def __init__(self, logger):
        self.logger = logger
        self.app = Flask(__name__)
        self.add_all_endpoints()
        self.URLAnalyser = URLAnalyser({}, logger=logger)

    def run(self):
        self.app.run(debug=True)

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
            result = self.URLAnalyser.is_malware(url)
            data = {
                "message": f"Is {url} a malware? {result}",
                "status": 200,
                "result": result,
            }
        return jsonify(data)
