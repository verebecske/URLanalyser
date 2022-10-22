import requests
import os
from flask import Flask, request, render_template, route

app = Flask(__name__)

def ask_urlanalyserapi(url: str) -> str:
    r = requests.get(f"{host}:{port}/check?url={url}")
    if r.status_code == 200:
        if r.json()["result"]:
            return "malware"
        return "not malware"
    return "unknown"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        url = request.form["url"]
        result = ask_urlanalyserapi(url)
        return render_template("return.html", name=name, url=url, result=result)
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
