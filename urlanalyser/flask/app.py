from flask import Flask, jsonify, request
from src.URLAnalyser import URLAnalyser
from logging import Logger


class FlaskAppWrapper(object):
    logger: Logger
    analyser: URLAnalyser

    def __init__(self, config: dict, analyser: URLAnalyser, logger: Logger):
        self.logger = logger
        self.app = Flask(__name__)
        self.add_all_endpoints()
        self.app.run(debug=bool(config["debug"]))

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
