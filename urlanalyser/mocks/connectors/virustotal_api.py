import json
import random
from src.connectors.virustotal_api import VirusTotalAPI as VirusTotal


class VirusTotalAPI(VirusTotal):
    def send_request(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            virustotal_ans = self.open_file("virustotal_ans.json")
            return virustotal_ans["data"]["attributes"]["last_analysis_stats"]
        return "error"

    def open_file(self, filename: str) -> dict:
        with open(f"datas/{filename}", "r") as file:
            return json.load(file)
