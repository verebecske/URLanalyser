import requests
import os
from flask import Flask, request, render_template

app = Flask(__name__)
host = "urlanalyser-urlanalyser-1"
port = os.getenv("URLANALYSER_PORT")

def ask_urlanalyserapi(url: str, settings: dict) -> dict:
    r = requests.get(f"http://{host}:{port}/check?url={url}")
    if r.status_code == 200 and r.json()["status"] == 200:
        return r.json() # ["result"]
    return {"result": "unknown"}



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        url = request.form["url"]
        urlhaus = request.form.get("urlhaus") != None
        virustotal = request.form.get("virustotal") != None
        geoip = request.form.get("geoip") != None
        screenshot = request.form.get("screenshot") != None
        checkedlist = [urlhaus, virustotal, geoip, screenshot]
        settings = {
            "urlhaus": urlhaus,
            "virustotal": virustotal,
            "geoip": geoip,
            "screenshot": screenshot
        }
        result = ask_urlanalyserapi(url, settings)
        return render_template("return.html", name=name, url=url, result=result, checkedlist=checkedlist)
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
