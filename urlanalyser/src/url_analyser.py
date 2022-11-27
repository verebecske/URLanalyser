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
        raise ValueError("not yet :(")

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None

    def collect_infos(self, url: str, datas: dict) -> dict:
        try:
            result = {}
            if self.valid_url(url):
                if "urlhaus" in datas.keys() and datas["urlhaus"] == True:
                    result["urlhaus"] = self.connector.send_request_to_urlhaus(url)
                if "virustotal" in datas.keys() and datas["virustotal"] == True:
                    result["virustotal"] = self.connector.send_request_to_virustotal(
                        url
                    )
                if "geoip" in datas.keys() and datas["geoip"] == True:
                    result["geoip"] = self.connector.get_geoip(url)
                if "history" in datas.keys() and datas["history"] == True:
                    result["history"] = self.malaut.get_repath(url)
                return result
        except Exception as e:
            return {"error": str(e)}

    def create_valid_url(self, url: str) -> str:
        if not valid_url(url):
            raise ValueError("not valid url")
        if not url.startswith("http"):
            url = "http://" + url
        return url
