import requests
import os
from flask import Flask, request, redirect
import csv
import json
import random

app = Flask(__name__)
config = {"host": "host", "port": "port"}


@app.route("/")
def home():
    # redirect version
    # return redirect(all_urls[0], code=302)
    malicious_url = get_malicious_url()
    html = f"<html><head>Are you sure?</head><body><p>Have fun!</p><a href={malicious_url}>{malicious_url}</a></body></html>"
    return html


@app.route("/fnet")
def home():
    malicious_url = get_malicious_url_from_file()
    html = f"<html><head>Are you sure?</head><body><p>Have fun!</p><a href={malicious_url}>{malicious_url}</a></body></html>"
    return html


def get_all_malicious_url() -> list:
    r = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
    content = r.text.replace("\r", "").split("\n")
    record = {}
    all_url = []
    for i in content:
        if i.startswith("#") or i == "":
            pass
        else:
            print(i.split('","'))
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
    with open("malicious_urls.csv", "w") as fd:
        fd.write(r.text)


def read_from_file_malicious_url() -> dict:
    with open("malicious_urls.csv", "r") as fd:
        reader = csv.reader(fd)
        dict_from_csv = {rows[0]: rows[1] for rows in reader}
    return dict_from_csv


def get_malicious_url_from_file() -> str:
    malur = read_from_file_malicious_url()


def get_malicious_url() -> str:
    all_url = get_all_malicious_url()
    rand = random.randint(0, len(all_url))
    return all_url[rand]


if __name__ == "__main__":
    write_file_malicious_url()
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)
