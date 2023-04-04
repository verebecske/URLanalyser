from src.ancestor import Ancestor
import requests
import re


class URLHausAPI(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request(self, url: str) -> dict:
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            return self.format_answer(response.json())           
        else:
            return {"error": response.text}

    def in_urlhaus_database(self, url: str) -> str:
        path = "urlhaus_database/csv.csv"
        with open(path) as file:
            for line in file:
                if not line.startswith("#") and not line == "":
                    datas = line.split('","')
                    (
                        id,
                        dateadded,
                        mal_url,
                        url_status,
                        last_online,
                        threat,
                        tags,
                        urlhaus_link,
                        reporter,
                    ) = datas
                    if url in mal_url:
                        return True
        return False

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

    def format_answer(self, response: dict) -> dict:
        query_status = response["query_status"]
        ans = {"query_status": query_status}
        if query_status == "ok":
            ans["threat"] = response["threat"]
            ans["url_status"] = response["url_status"]
        return ans

    def update_urlhaus_database(self) -> None:
        r = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
        with open("urlhaus_database/malicious_urls.csv", "w") as fd:
            fd.write(r.text)
        self.logger.info("URLHaus database updated")