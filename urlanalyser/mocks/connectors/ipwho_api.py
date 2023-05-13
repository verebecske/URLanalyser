import json
import random
from src.connectors.ipwho_api import IPWhoAPI as IPWho


class IPWhoAPI(IPWho):
    def get_ip(self, url: str) -> str:
        return "127.0.0.1"

    def get_location(self, url: str) -> str:
        if random.randint(0, 100) < 70:
            return self.open_file("location_valid.json")["country"]
        return "error"
