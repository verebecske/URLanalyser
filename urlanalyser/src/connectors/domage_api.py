from src.ancestor import Ancestor
import re
import socket
import requests


class DomageAPI(Ancestor):
    def __init__(self, config: dict):
        super().__init__()

    def get_domain(self, url: str) -> str:
        pattern = r"(http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+"
        domain = re.match(pattern, url)[0]
        if "http" in domain:
            domain = domain.split("//")[1]
        return domain

    def get_domain_age(self, url: str) -> dict:
        domain = self.get_domain(url)
        response = requests.get(
            f"https://ipty.de/domage/api.php?domain={domain}&mode=full", verify=False
        )
        if response.status_code == 200:
            return self.format_answer(response.json())
        else:
            return {"error": response.text}

    def format_answer(self, response: dict) -> dict:
        res = response["result"]["creation"]
        res.pop("classification", None)
        field = res.pop("field", "date")
        new_field = "".join(char for char in field if char.isalnum() or char == " ")
        date = res.pop("date", "unknown")
        res[new_field] = date
        return res
