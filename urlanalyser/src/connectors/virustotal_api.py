from src.ancestor import Ancestor


class VirusTotalAPI(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def send_request(self, url: str) -> dict:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_key = self.config["virustotal_api_key"]
        headers = {"accept": "application/json", "x-apikey": api_key}
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers
        )
        if response.status_code == 200:
            return response.json()["data"]["attributes"]["last_analysis_stats"]
        else:
            return {"error": response.text}
