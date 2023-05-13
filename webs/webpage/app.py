import requests
import base64
import os
from flask import Flask, request, render_template


class FlaskWebPage:
    debug: bool
    config: dict

    def __init__(self, config: dict):
        self.config = config
        self.app = Flask(__name__)
        self.analyser = (
            f'http://{self.config["analyser_host"]}:{self.config["analyser_port"]}'
        )
        self._add_all_endpoints()
        # self._add_errors()

    def run(self) -> None:
        host = self.config["host"]
        port = self.config["port"]
        self.app.run(debug=False, host=host, port=port)

    def _add_all_endpoints(self):
        self.app.add_url_rule("/", "index", self.index, methods=["GET", "POST"])

    # def _add_errors(self) -> None:
    #     self.app.register_error_handler(400, self._handle_bad_request)
    #     self.app.register_error_handler(500, self._handle_internal_server_error)
    #     self.app.register_error_handler(405, self._handle_method_not_allowed)
    #     self.app.register_error_handler(404, self._handle_not_found)

    def index(self):
        if request.method == "POST":
            return self.post_index()
        return self.get_index()

    def get_index(self):
        return render_template("home.html")

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()

    def ask_urlanalyserapi(self, settings: dict) -> dict:
        response = requests.post(f"{self.analyser}/get_info", json=settings)
        if response.status_code == 200:
            return response.json()["result"]
        return {"result": ""}

    def get_screenshot(self, url: str) -> str:
        url = self._encode_url(url)
        response = requests.get(f"{self.analyser}/get_screenshot?url={url}")
        path = "./static/screenshot.png"
        with open(path, "wb") as image_file:
            image_file.write(response.content)
        return "screenshot.png"

    def get_settings_from_form(self, request):
        settings = {
            "url": request.form.get("url", ""),
            "urlhaus": request.form.get("urlhaus", False),
            "virustotal": request.form.get("virustotal", False),
            "location": request.form.get("location", False),
            "screenshot": request.form.get("screenshot", False),
            "redirection": request.form.get("redirection", False),
        }
        return settings

    def post_index(self):
        settings = self.get_settings_from_form(request)
        if settings["url"] == "":
            return render_template("home.html", error="Missing URL")
        result = self.ask_urlanalyserapi(settings)
        filename = ""
        if settings["screenshot"]:
            filename = self.get_screenshot(settings["url"])
        return render_template(
            "return.html", url=settings["url"], result=result, filename=filename
        )


if __name__ == "__main__":
    config = {
        "host": "0.0.0.0",
        "port": os.getenv("PORT"),
        "analyser_host": "urlanalyser-urlanalyser-1",
        "analyser_port": os.getenv("URLANALYSER_PORT"),
    }
    flaskapp = FlaskWebPage(config)
    flaskapp.run()
