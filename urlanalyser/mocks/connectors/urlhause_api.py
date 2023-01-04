import json
import random
from src.connectors.urlhause_api import URLHausAPI as URLHaus


class URLHausAPI(URLHaus):
    def send_request(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            mock_resp = self.open_file("urlhaus_online.json")
            query_status = mock_resp["query_status"]
            ans = {"query_status": query_status}
            if query_status == "ok":
                ans["threat"] = mock_resp["threat"]
                ans["url_status"] = mock_resp["url_status"]
            return ans
        return "error"
