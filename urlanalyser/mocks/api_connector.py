import json
import random
from src.api_connector import APIConnector as Connector


class APIConnector(Connector):
    def send_request_to_virustotal(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            return self.open_file("virustotal_ans.json")["attributes"][
                "last_analysis_stats"
            ]
        return "error"

    def send_request_to_urlhaus(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            mock_resp = self.open_file("urlhaus_online.json")
            query_status = mock_resp["query_status"]
            ans = {"query_status": query_status}
            if query_status == "ok":
                ans["threat"] = mock_resp["threat"]
                ans["url_status"] = mock_resp["url_status"]
            return ans
        return "error"

    def get_ip(self, url: str) -> str:
        return "127.0.0.1"

    def get_geoip(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            return self.open_file("geoip_valid.json")["country"]
        return "error"

    def open_file(self, filename: str) -> dict:
        with open(f"datas/{filename}", "r") as file:
            return json.load(file)
