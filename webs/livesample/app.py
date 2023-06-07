import requests
import os
from flask import Flask, request, redirect
import random

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
    response = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
    content = response.text.replace("\r", "").split("\n")
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
    response = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
    with open("urlhaus_database/malicious_urls.csv", "w") as fd:
        fd.write(response.text)


def read_from_file_malicious_url() -> str:
    path = "urlhaus_database/csv.csv"
    record = {}
    all_url = []
    with open(path) as file:
        for line in file:
            if not line.startswith("#") and not line == "":
                datas = line.split('","')
                (
                    id,
                    dateadded,
                    url,
                    url_status,
                    last_online,
                    threat,
                    tags,
                    urlhaus_link,
                    reporter,
                ) = datas
                record[id.replace('"', "")] = {
                    "id": id.replace('"', ""),
                    "url": url,
                    "threat": threat,
                    "tags": tags,
                }
                all_url.append(url)
    return all_url


def get_malicious_url_from_file() -> str:
    all_url = read_from_file_malicious_url()
    rand = random.randint(0, len(all_url))
    return all_url[rand]


def get_malicious_url() -> str:
    all_url = get_all_malicious_url()
    rand = random.randint(0, len(all_url))
    return all_url[rand]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
