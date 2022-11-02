import requests
import os
from flask import Flask, request, redirect
import json
import random
import pandas as pd

app = Flask(__name__)

@app.route("/now")
def home():
    malicious_url = get_malicious_url()
    html = f"<html><head>Are you sure?</head><body><p>Have fun!</p><a href={malicious_url}>{malicious_url}</a></body></html>"
    return html


@app.route("/")
def cache_home():
    malicious_url = get_malicious_url_from_file()
    html = f"<html><head>Are you sure?</head><body><p>Have fun!</p><a href={malicious_url}>{malicious_url}</a></body></html>"
    return html


@app.route("/reset")
def reset_db():
    write_file_malicious_url()
    return redirect(url_for(""))


def get_all_malicious_url() -> list:
    r = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
    content = r.text.replace("\r", "").split("\n")
    record = {}
    all_url = []
    for i in content:
        if not i.startswith("#") and not i == "":
            datas = i.split('","')
            id, dateadded, url, url_status, threat, tags, urlhaus_link, reporter = datas
            record[id.replace('"', "")] = {
                "id": id.replace('"', ""),
                "url": url,
                "threat": threat,
                "tags": tags,
            }
            all_url.append(url)
    return all_url


def write_file_malicious_url() -> None:
    r = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
    with open("urlhaus_database/malicious_urls.csv", "w") as fd:
        fd.write(r.text)


def read_from_file_malicious_url() -> str:
    dict_from_csv = pd.read_csv(
        "urlhaus_database/malicious_urls.csv",
        header=None,
        index_col=0,
        skip_blank_lines=True,
        comment="#",
    )
    return dict_from_csv[2].sample().iloc[0]


def get_malicious_url_from_file() -> str:
    malur = read_from_file_malicious_url()
    return str(malur)


def get_malicious_url() -> str:
    all_url = get_all_malicious_url()
    rand = random.randint(0, len(all_url))
    return all_url[rand]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
