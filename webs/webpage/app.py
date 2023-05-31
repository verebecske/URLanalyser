import requests
import base64
import os
from flask import Flask, request, render_template, send_from_directory


class FlaskWebPage:
    debug: bool
    config: dict

    def __init__(self, config: dict, urlanalyser):
        self.config = config
        self.app = Flask(__name__)
        self._add_all_endpoints()
        self.urlanalyser = urlanalyser

    def run(self) -> None:
        host = self.config["host"]
        port = self.config["port"]
        self.app.run(debug=config["debug"], host=host, port=port)

    def _add_all_endpoints(self):
        self.app.add_url_rule("/", "index", self.index, methods=["GET", "POST"])
        self.app.add_url_rule("/downloadzip", "downloadzip", self.download_as_zip,  methods=["GET"])

    def index(self):
        if request.method == "POST":
            return self.post_index()
        return self.get_index()

    def get_index(self):
        return render_template("home.html")

    def get_settings_from_form(self, request):
        settings = {
            "url": request.form.get("url", ""),
            "urlhaus": request.form.get("urlhaus", False),
            "virustotal": request.form.get("virustotal", False),
            "location": request.form.get("location", False),
            "screenshot": request.form.get("screenshot", False),
            "redirection": request.form.get("redirection", False),
            "red_all": request.form.get("red_all", False),
            "domain_age": request.form.get("domain_age", False),
            "domain_reputation": request.form.get("domain_reputation", False),
            "download": request.form.get("download", False)
        }
        return settings

    def download_as_zip(self):
        return send_from_directory("./static/", "page.zip", as_attachment=True)

    def post_index(self):
        settings = self.get_settings_from_form(request)
        if settings["url"] == "":
            return render_template("home.html", error="Missing URL")
        result = self.urlanalyser.ask_urlanalyserapi(settings)
        filename = ""
        download = ""
        is_malicious = self.urlanalyser.check_url(settings["url"])
        if settings["screenshot"]:
            filename = self.urlanalyser.get_screenshot(settings["url"])
        if settings["download"]:
            download = self.urlanalyser.download_as_zip(settings["url"])
        return render_template(
            "return.html", url=settings["url"], result=result, filename=filename, 
            download=download, is_malicious=is_malicious
        )


class URLAnalyserAPI:
    def __init__(self, config: dict):
        if config["analyser_host"] is None:
            raise Exception("Missing URLAnalasyer host")
        self.urlanalyser_url = (
            f'http://{config["analyser_host"]}:{config["analyser_port"]}'
        )

    def ask_urlanalyserapi(self, settings: dict) -> dict:
        result = {}
        url = settings["url"]
        result.update(self.get_info(settings))
        if settings["redirection"]:
            result["redirection"] = self._redirection_handler(url, settings["red_all"])
        if settings["domain_age"]:
            result["domain_age"] = self.domain_age_handler(url)
        if settings["domain_reputation"]:
            result["domain_reputation"] = self.domain_reputation_handler(url)
        return result

    def get_info(self, settings: dict) -> dict:
        response = requests.post(f"{self.urlanalyser_url}/get_info", json=settings)
        if response.status_code == 200:
            return response.json()["result"]
        return {"result": f"Server error happened: {response.text}"}

    def check_url(self, url: str) -> bool:
        try:
            result = self.send_get_request("check", url)
            return result.json()["result"]["is_malicious"]
        except Exception as error:
            pass
        return False

    def domain_age_handler(self, url):
        return self.send_get_request("get_domain_age", url)

    def domain_reputation_handler(self, url):
        return self.send_get_request("get_domain_reputation", url)

    def _redirection_handler(self, url, content):
        if content:
            extras = {"all": "True"}
        else:
            extras = None
        return self.send_get_request("get_redirection", url, extras)

    def _location_handler(self, urls, channel):
        return self.send_get_request("get_location", url)

    def send_get_request(self, endpoint, url, extras: dict = None):
        if extras is None:
            _extras = ""
        else:
            _extras = "".join([f"&{key}={value}" for key, value in extras.items()])
        url = self._encode_url(url)
        response = requests.get(f"{self.urlanalyser_url}/{endpoint}?url={url}{_extras}")
        if response.status_code == 200:
            return response.json()["result"]
        else:
            return {"result": f"Server error happened: {response.text}"}

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()

    def get_screenshot(self, url: str) -> str:
        url = self._encode_url(url)
        response = requests.get(f"{self.urlanalyser_url}/get_screenshot?url={url}")
        if response.status_code == 200:
            path = "./static/screenshot.png"
            with open(path, "wb") as image_file:
                image_file.write(response.content)
            return "screenshot.png"
        else:
            raise ServerError(f"Something went wrong with: {url}")

    def download_as_zip(self, url: str):
        url = self._encode_url(url)
        response = requests.get(f"{self.urlanalyser_url}/download_as_zip?url={url}")
        if response.status_code == 200:
            path = "./static/page.zip"
            with open(path, "wb") as image_file:
                image_file.write(response.content)
            return "page.zip"
        else:
            raise ServerError(f"Something went wrong with: {url}")

if __name__ == "__main__":
    config = {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": os.getenv("PORT", 5000),
        "analyser_host": os.getenv("URLANALYSER_HOST"),
        "analyser_port": os.getenv("URLANALYSER_PORT"),
        "debug": os.getenv("DEBUG")
    }
    urlanalyser = URLAnalyserAPI(config)
    flaskapp = FlaskWebPage(config, urlanalyser)
    flaskapp.run()
