import json
from src.url_analyser import URLAnalyser as Analyser


class URLAnalyser(Analyser):
    def is_malware(self, url: str) -> bool:
        return random.randint(0, 100) < 70
