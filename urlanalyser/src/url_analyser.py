import re
import uuid
from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhaus_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.connectors.apivoid_api import APIVoidAPI
from src.connectors.redis_database import RedisDatabase
from src.connectors.domage_api import DomageAPI
from src.connectors.collector import Collector
from src.ancestor import Ancestor
from src.malaut import Malaut


class URLAnalyser(Ancestor):
    def __init__(
        self,
        config: dict,
        ipwho_api: IPWhoAPI,
        urlhaus_api: URLHausAPI,
        virustotal_api: VirusTotalAPI,
        apivoid_api: APIVoidAPI,
        domage_api: DomageAPI,
        malaut: Malaut,
        collector: Collector,
        redis: RedisDatabase,
    ):
        super().__init__()
        self.ipwho_api = ipwho_api
        self.urlhaus_api = urlhaus_api
        self.virustotal_api = virustotal_api
        self.domage_api = domage_api
        self.apivoid_api = apivoid_api
        self.malaut = malaut
        self.collector = collector
        self.redis = redis

    def is_malware(self, url: str) -> bool:
        return self.urlhuas_api.in_urlhaus_database(url)

    def valid_url(self, url: str) -> bool:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?$"
        res = re.match(pattern, url)
        return res != None

    def collect_infos(self, url: str, datas: dict) -> dict:
        result = {}
        if self.valid_url(url):
            if "urlhaus" in datas.keys() and not datas["urlhaus"] == False:
                result["urlhaus"] = self.urlhaus_api.send_request(url)
            if "virustotal" in datas.keys() and not datas["virustotal"] == False:
                result["virustotal"] = self.virustotal_api.send_request(url)
            if "location" in datas.keys() and not datas["location"] == False:
                result["location"] = self.get_location(url)
            if "redirection" in datas.keys() and not datas["redirection"] == False:
                url = self.create_valid_url(url)
                result["redirection"] = self.get_redirection(url, "False")
            if "domain_age" in datas.keys() and not datas["domain_age"] == False:
                result["domain_age"] = self.get_domain_age(url)
            if (
                "domain_reputation" in datas.keys()
                and not datas["domain_reputation"] == False
            ):
                result["domain_reputation"] = self.get_domain_reputation(url)
            return result
        else:
            raise ValueError("invalid URL")

    def get_redirection(self, url, verbosity: str = ""):
        _all = verbosity.lower() in ["true", "y", "yes"]
        url = self.create_valid_url(url)
        return self.malaut.get_redirection(url, all=_all)

    def get_location(self, url):
        return self.ipwho_api.get_location(url)

    def get_domain_age(self, url):
        return self.domage_api.get_domain_age(url)

    def get_domain_reputation(self, url):
        ip = self.ipwho_api.get_ip(url)
        res = self.collector.check_ip_reputation(ip)
        if res == []:
            return {"Block list in": "none of known list"}
        else:
            strlist = ",".join(res)
            return {"Block list in": strlist}

    def create_zip(self, url):
        filename = str(uuid.uuid4())[:8] + "_page.zip"
        path = "./src/flask/static/" + filename
        url = self.create_valid_url(url)
        self.malaut.create_zip_with_selenium(url, path)
        return filename

    def create_valid_url(self, url: str) -> str:
        if not url.startswith("http"):
            url = "http://" + url
        if not self.valid_url(url):
            raise ValueError("invalid URL")
        return url

    def create_screenshot(self, url: str) -> str:
        filename = str(uuid.uuid4())[:8] + "_screenshot.png"
        path = "./src/flask/static/" + filename
        url = self.create_valid_url(url)
        self.malaut.create_screenshot(url, path)
        return filename

    def check(self, url: str) -> str:
        result = {}
        result["is_malicious"] = self.majority_gate(url)
        return result

    def majority_gate(self, url: str):
        UH = self.urlhaus_api.get_is_malicous_result(url)
        VT = self.virustotal_api.get_is_malicous_result(url)
        ip = self.ipwho_api.get_ip(url)
        IV = self.collector.get_is_malicous_result(ip, url)
        return (UH and VT) or (IV and VT) or (IV and UH)

    def create_data_to_redis(self, url: str) -> dict:
        pass
