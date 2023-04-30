from flask import Flask, jsonify, request, send_from_directory
import base64
from src.url_analyser import URLAnalyser
from src.malaut import Malaut
from src.ancestor import Ancestor
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
from enum import Enum


class BadRequestType(Enum):
    MISSING_URL = "Missing URL"
    INVALID_URL = "Invalid URL"
    INVALID_CONTENT_TYPE = "Invalid Content-Type"


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
        self._add_all_endpoints()
        self._add_errors()

    def run(self) -> None:
        host = self.config["host"]
        port = self.config["port"]
        self.app.run(debug=False, host=host, port=port)

    def _add_all_endpoints(self):
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/check", "check", self.check, methods=["GET", "POST"])
        self.app.add_url_rule(
            "/get_screenshot", "get_screenshot", self.get_screenshot, methods=["GET"]
        )
        self.app.add_url_rule(
            "/get_history", "get_history", self.get_history, methods=["GET"]
        )
        self.app.add_url_rule(
            "/get_infos", "get_infos", self.get_infos, methods=["POST"]
        )

    def _add_errors(self) -> None:
        self.app.register_error_handler(400, self._handle_bad_request)
        self.app.register_error_handler(500, self._handle_internal_server_error)
        self.app.register_error_handler(405, self._handle_method_not_allowed)
        self.app.register_error_handler(404, self._handle_not_found)

    def _handle_bad_request(self, error):
        self.logger.error(f"Handle: {error}")

        if error.description in BadRequestType:
            return f"bad request - {error.description.value}", 400
        return "bad request", 400

    def _handle_internal_server_error(self, error):
        return "internal server error", 500

    def _handle_method_not_allowed(self, error):
        return "method not allowed", 405

    def _handle_not_found(self, error):
        return "not found", 404

    def _get_url_from_get_request(self) -> str:
        url = request.args.get("url", default="")
        if url == "":
            raise BadRequest(description=BadRequestType.MISSING_URL)
        url = self._decode_url(url)
        if not self.analyser.valid_url(url):
            raise BadRequest(description=BadRequestType.INVALID_URL)
        return url

    def _get_url_from_post_request(self) -> str:
        try:
            data = request.json
        except:
            raise BadRequest(description=BadRequestType.INVALID_CONTENT_TYPE)
        if "url" not in data or data["url"] == "":
            raise BadRequest(description=BadRequestType.MISSING_URL)
        if not self.analyser.valid_url(data["url"]):
            raise BadRequest(description=BadRequestType.INVALID_URL)
        return data["url"]

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()

    def get_infos(self):
        try:
            self.logger.info(f"Get request: {request.json}")
            data = request.json
            url = self._get_url_from_post_request()
            result = self.analyser.collect_infos(data["url"], data)
            response = {
                "url": data["url"],
                "result": result,
            }
            return jsonify(response), 200
        except BadRequest as error:
            raise
        except Exception as error:
            self.logger.error(f"Error occured while gathering infos: {error}")
            raise InternalServerError()

    def index(self):
        self.logger.info(f"Get request: {request.data}")
        response = {"message": "Live long and prosper!"}
        return jsonify(response), 200

    def check(self):
        try:
            self.logger.info(f"Get request: {request.data}")
            if request.method == "GET":
                url = self._get_url_from_get_request()
            else:
                url = self._get_url_from_post_request()
            result = self.analyser.check(url)
            response = {"result": result, "url": self._encode_url(url)}
            return jsonify(response), 200
        except BadRequest as error:
            raise
        except Exception as error:
            self.logger.error(f"Error occured while checking url: {error}")
            raise InternalServerError()

    def get_screenshot(self):
        try:
            self.logger.info(f"Get request: {request.data}")
            url = self._get_url_from_get_request()
            path = self.analyser.create_screenshot(url)
            return send_from_directory("/src/flask/static/", path, as_attachment=True)
        except BadRequest as error:
            raise
        except Exception as error:
            self.logger.error(f"Error occured while creating screenshot: {error}")
            raise InternalServerError()

    def get_history(self):
        try:
            self.logger.info(f"Get request: {request.json}")
            url = self._get_url_from_get_request()
            path_list = self.analyser.get_history(url)
            return jsonify({"result": path_list, "url": self._encode_url(url)}), 200
        except BadRequest as error:
            raise
        except Exception as error:
            self.logger.error(f"Error occured while checking url history: {error}")
            raise InternalServerError()
