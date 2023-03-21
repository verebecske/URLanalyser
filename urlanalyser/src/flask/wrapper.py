from flask import Flask, jsonify, request, send_from_directory
import base64
from src.url_analyser import URLAnalyser
from src.malaut import Malaut
from src.ancestor import Ancestor


class FlaskAppWrapper(Ancestor):
    analyser: URLAnalyser
    debug: bool
    config: dict

    def __init__(self, config: dict, analyser: URLAnalyser):
        super().__init__()
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
        self.app.add_url_rule("/check", "check", self.check, methods=["GET", "POST"])
        self.app.add_url_rule(
            "/image", "get_screenshot", self.get_screenshot, methods=["GET"]
        )
        self.app.add_url_rule(
            "/get_repath", "get_repath", self.get_repath, methods=["GET"]
        )
        self.app.add_url_rule(
            "/get_infos", "get_infos", self.get_infos, methods=["POST"]
        )

    def get_infos(self):
        try:
            self.logger.info(request.json)
            datas = request.json
            status = 200
            if "url" not in datas or datas["url"] == "":
                status = 400
                data = {
                    "message": "Bad request!",
                    "Error": "Unexpected error.",
                }
            else:
                result = self.analyser.collect_infos(datas["url"], datas)
                data = {
                    "url": datas["url"],
                    "result": result,
                }
            return jsonify(data), status
        except Exception as e:
            self.logger.error(e)
            return jsonify({"error": e}), 400

    def index(self):
        data = {
            "message": f"Hallo Welt",
            "status": 200,
        }
        return jsonify(data)

    def check(self):
        try:
            url = self._get_url_from_get_request()
            result = self.analyser.check(url)
            data = {"result": result, "url": self._encode_url(url)}
            return jsonify(data), 200
        except Exception as e:
            self.logger.error(e)
            data = {"error": "Somethings went wrong...", "url": self._encode_url(url)}
            return jsonify(data), 400

    def get_screenshot(self):
        url = self._get_url_from_get_request()
        path = self.analyser.create_screenshot(url)
        try:
            return send_from_directory("/src/flask/static/", path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    def get_repath(self):
        url = self._get_url_from_get_request()
        path_list = self.analyser.get_repath(url)
        return jsonify({"path": path_list})

    def _get_url_from_get_request(self) -> str:
        url = request.args.get("url", default=b"")
        return self._decode_url(url)

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()
