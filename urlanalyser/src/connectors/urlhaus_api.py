from src.ancestor import Ancestor
import requests
import re


class URLHausAPI(Ancestor):
    config: dict
    path: str

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.path = "static_database/urlhaus/csv.csv"

    def send_request(self, url: str) -> dict:
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def get_is_malicous_result(self, url) -> bool:
        result = self.send_request(url)
        try:
            match response["query_status"]:
                case "invalid_url":
                    return False
                case "no_result":
                    return False
                case "ok":
                    return True
        except:
            pass
        return True

    def in_urlhaus_database(self, url: str) -> bool:
        with open(self.path) as file:
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

    def get_urlhaus_database(self, url: str):
        try:
            with open(self.path) as file:
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
                            return datas
        except OSError as error:
            self.logger.error(error)
        return None

    def read_from_file_malicious_url() -> list:
        record = {}
        all_url = []
        with open(self.path) as file:
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
        response = requests.get(url="https://urlhaus.abuse.ch/downloads/csv_online/")
        with open("static_database/urlhaus/malicious_urls.csv", "w") as fd:
            fd.write(response.text)
        self.logger.info("URLHaus database updated")
