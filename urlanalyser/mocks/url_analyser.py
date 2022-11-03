import json
from src.url_analyser import URLAnalyser as Analyser


class URLAnalyser(Analyser):
    def is_malware(self, url: str) -> bool:
        return random.randint(0, 100) < 70

    def collect_infos(self, url: str, sets: str) -> dict:
        if self.valid_url(url):
            result = {}
            if sets[0] == "1":
                result["urlhaus"] = self.open_file("urlhaus_online.json")
            if sets[1] == "1":
                result["virustotal"] = self.open_file("virustotal_ans.json")
            if sets[2] == "1":
                result["geoip"] = self.open_file("geoip_valid.json")
            return result
        return {"error": "error"}

    def open_file(self, filename: str) -> dict:
        with open(f"datas/{filename}", "r") as file:
            return json.load(file)
