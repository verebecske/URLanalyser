import os
import datetime
import requests
from flask import Flask, jsonify, request, render_template, send_from_directory
import base64
from src.url_analyser import URLAnalyser
from src.malaut import Malaut
from src.ancestor import Ancestor
from splinter import Browser


class FlaskAppWrapper(Ancestor):
    analyser: URLAnalyser
    debug: bool
    config: dict

    def __init__(self, config: dict, analyser: URLAnalyser):
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
        self.app.add_url_rule("/get_repath", "get_repath", self.get_repath)

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

    def get_screenshot(self):
        url = request.args.get("url", default="", type=str)
        path = self.analyser.create_screenshot(url)
        try:
            return send_from_directory("/src/flask/static/", path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    def get_repath(self):
        url = request.args.get("url", default="", type=str)
        path_list = self.analyser.get_repath(url)
        return jsonify({"path": path_list})
