import requests
import os
from flask import Flask, request, render_template

app = Flask(__name__)
host = "urlanalyser-urlanalyser-1"
port = os.getenv("URLANALYSER_PORT")


def encode_settings(settings: dict) -> str:
    res = [
        int(settings["urlhaus"]),
        int(settings["virustotal"]),
        int(settings["geoip"]),
    ]
    return "".join([str(i) for i in res])


def ask_urlanalyserapi(datas: dict) -> dict:
    # est = encode_settings(settings)
    r = requests.post(f"http://{host}:{port}/get_infos", json=datas)
    if r.status_code == 200:
        return r.json()["result"]
    return {"result": ""}


def get_screenshot(url: str) -> str:
    r = requests.get(f"http://{host}:{port}/get_screenshot?url={url}")
    path = "./static/screenshot.png"
    with open(path, "wb") as image_file:
        image_file.write(r.content)
    return "screenshot.png"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        url = request.form["url"]
        urlhaus = request.form.get("urlhaus", False)
        virustotal = request.form.get("virustotal", False)
        geoip = request.form.get("geoip", False)
        screenshot = request.form.get("screenshot", False)
        history = request.form.get("history", False)
        data = {
            "url": url,
            "urlhaus": urlhaus,
            "virustotal": virustotal,
            "geoip": geoip,
            "screenshot": screenshot,
            "history": history,
        }
        result = ask_urlanalyserapi(data)
        filename = ""
        if screenshot:
            filename = get_screenshot(url)
        return render_template(
            "return.html", name=name, url=url, result=result, filename=filename
        )
    else:
        return render_template("home.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/test", methods=["GET"])
def get_image():
    r = requests.get(f"http://{host}:{port}/get_screenshot")
    path = "./static/screenshot.png"
    with open(path, "wb") as image_file:
        image_file.write(r.content)
    return render_template("image.html", path="screenshot.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
