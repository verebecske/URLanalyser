import re
from src.api_connector import APIConnector
from src.ancestor import Ancestor
from src.malaut import Malaut


class URLAnalyser(Ancestor):
    connector: APIConnector

    def __init__(self, config: dict, connector: APIConnector, malaut: Malaut):
        super().__init__()
        self.connector = connector
        self.malaut = malaut

    def is_malware(self, url: str) -> bool:
        return self.in_urlhaus_database(url)

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None

    def collect_infos(self, url: str, datas: dict) -> dict:
        result = {}
        if self.valid_url(url):
            if "urlhaus" in datas.keys() and not datas["urlhaus"] == False:
                result["urlhaus"] = self.connector.send_request_to_urlhaus(url)
            if "virustotal" in datas.keys() and not datas["virustotal"] == False:
                result["virustotal"] = self.connector.send_request_to_virustotal(url)
            if "geoip" in datas.keys() and not datas["geoip"] == False:
                result["geoip"] = self.connector.get_geoip(url)
            if "history" in datas.keys() and not datas["history"] == False:
                url = self.create_valid_url(url)
                result["history"] = self.malaut.get_repath(url)
            return result

    def create_valid_url(self, url: str) -> str:
        if not self.valid_url(url):
            raise ValueError("not valid url")
        if not url.startswith("http"):
            url = "http://" + url
        return url

    def create_screenshot(self, url: str) -> str:
        filename = "screenshot.png"
        path = "./src/flask/static/" + filename
        url = self.create_valid_url(url)
        self.malaut.create_screenshot(url, path)
        return filename

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
