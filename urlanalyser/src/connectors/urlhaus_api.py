from src.ancestor import Ancestor
import requests

class URLHausAPI(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request(self, url: str) -> dict:
        data = {"url": url}
        response = requests.post(url="https://urlhaus-api.abuse.ch/v1/url/", data=data)
        if response.status_code == 200:
            query_status = response.json()["query_status"]
            ans = {"query_status": query_status}
            if query_status == "ok":
                ans["threat"] = response.json()["threat"]
                ans["url_status"] = response.json()["url_status"]
            return ans
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

