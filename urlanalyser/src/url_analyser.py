import re
import uuid
import hashlib
from logging import DEBUG
from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhaus_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.connectors.ip2location import IP2LocationAPI
from src.connectors.domage_api import DomageAPI
from src.connectors.collector import Collector
from src.ancestor import Ancestor
from src.sample_analyser import SampleAnalyser


class URLAnalyser(Ancestor):
    def __init__(
        self,
        config: dict,
        ipwho_api: IPWhoAPI,
        urlhaus_api: URLHausAPI,
        virustotal_api: VirusTotalAPI,
        ip2location: IP2LocationAPI,
        domage_api: DomageAPI,
        sample_analyser: SampleAnalyser,
        collector: Collector,
    ):
        super().__init__()
        self.ipwho_api = ipwho_api
        self.urlhaus_api = urlhaus_api
        self.virustotal_api = virustotal_api
        self.domage_api = domage_api
        self.ip2location = ip2location
        self.sample_analyser = sample_analyser
        self.collector = collector
        self.temp_folder = "./src/flask/static/"
        self.collection_database = []
        self.config = config
        if config["debug"] == "true":
            self.logger.setLevel(DEBUG)

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
        return self.sample_analyser.get_redirection(url, all=_all)

    def get_location(self, url):
        if "use_ip2location" in self.config:
            return self.ip2location.get_location(url)
        return self.ipwho_api.get_location(url)

    def get_domain_age(self, url):
        return self.domage_api.get_domain_age(url)

    def get_domain_reputation(self, url):
        ip = self.ipwho_api.get_ip(url)
        res = self.collector.check_ip_reputation(ip)
        res += self.collector.check_url_reputation(url)
        if res == []:
            return {"Block list in": "none of known list"}
        else:
            strlist = ", ".join(res)
            return {"Block list in": strlist}

    def create_zip(self, url):
        filename = str(uuid.uuid4())[:8] + "_page.zip"
        path = self.temp_folder + filename
        url = self.create_valid_url(url)
        self.sample_analyser.create_zip_with_selenium(url, path)
        return filename

    def add_to_malware_collection(self, url):
        self.collection_database.append(url)

    # TODO: nem a flask hiv erre ra, hanem belulrol hivodik meg ha karos dolgot talal es olyan meg nincs
    # TODO: kivulrol hivhato, de nem adja vissza a letoltott file-t
    # TODO: egy endpoint megmondja milyen gyujtemeny van - csak a nevuket
    def collect_malware_sample(self, url: str, path: str):
        filename = hashlib.md5(url.encode()).hexdigest() + "_sample.zip"
        path = path + filename
        url = self.create_valid_url(url)
        self.sample_analyser.collect_malware_sample(url, path)
        return filename

    def create_valid_url(self, url: str) -> str:
        if not url.startswith("http"):
            url = "http://" + url
        if not self.valid_url(url):
            raise ValueError("invalid URL")
        return url

    def create_screenshot(self, url: str) -> str:
        filename = str(uuid.uuid4())[:8] + "_screenshot.png"
        path = self.temp_folder + filename
        url = self.create_valid_url(url)
        self.sample_analyser.create_screenshot(url, path)
        return filename

    def check(self, url: str) -> str:
        result = {}
        result["is_malicious"] = self.majority_gate(url)
        if result["is_malicious"]:
            self.add_to_malware_collection(url)
        return result

    def majority_gate(self, url: str):
        UH = self.urlhaus_api.get_is_malicous_result(url)
        VT = self.virustotal_api.get_is_malicous_result(url)
        ip = self.ipwho_api.get_ip(url)
        IV = self.collector.get_is_malicous_result(ip, url)
        return (UH and VT) or (IV and VT) or (IV and UH)
