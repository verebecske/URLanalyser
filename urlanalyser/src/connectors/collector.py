from src.ancestor import Ancestor
import requests
import ipaddress
from collections import defaultdict
import re

class LocalResponse():
    text: str

class Collector(Ancestor):
    def __init__(self, blocklistdb):
        super().__init__()
        self.blocklistdb = blocklistdb

    def check_ip_reputation(self, ip: str) -> list:
        ip_addr = ipaddress.ip_address(ip)
        return self.blocklistdb.get_from_database("ip", ip)

    def check_url_reputation(self, url: str) -> list:
        return self.blocklistdb.get_from_database("url", url)

    def get_is_malicous_result(self, ip, url) -> bool:
        return (
            self.blocklistdb.get_from_database("ip", ip) != []
            or self.blocklistdb.get_from_database("url", url) != []
        )

    def send_request_and_save_result(self, url, filename, list_type, display_name):
        response = requests.get(url=url)
        with open(f"static_database/{filename}", "w") as fd:
            fd.write(response.text)
        for line in response.text.split("\n"):
            if line.startswith("#"):
                continue
            line = line.strip(" \r\n\t")
            try:
                if list_type == "ip":
                    match = re.search((r"((\d+).)*\d+"), line)
                    if match:
                        ip = ipaddress.ip_address(match.group(0))
                        self.blocklistdb.add_to_database("ip", ip, display_name)
                if list_type == "url":
                    self.blocklistdb.add_to_database("url", line, display_name)
            except ValueError as error:
                self.logger.warning(f"line: {line} error {error}")

    def collect_many(self):
        source = {
            "mirai": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://mirai.security.gives/data/ip_list.txt",
                "name": "Mirai Tracker",
            },
            "nubi_network": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://www.nubi-network.com/list.txt",
                "name": "NUBI",
            },
            "liquidbinary": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://liquidbinary.com/blackIPs.txt",
                "name": "Liquid Binary",
            },
            "sigs_interserver": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://sigs.interserver.net/iprbl.txt",
                "name": "InterServer"
            },
            "blisxfr": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://bl.isx.fr/raw",
                "name": "ISX.fr"
            },
            "blacklists": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://blacklists.co/download/all.txt",
                "name": "Blacklists.co",
            },
            "threat sourcing": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://www.threatsourcing.com/ipall.txt",
                "name": "Theat Sourcing"
            },
            "feodo": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt",
                "name": "Feodo Tracker",
            },
            "charles_haleys": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://charles.the-haleys.org/ssh_dico_attack_with_timestamps.php?days=1",
                "name": "Charles B. Haley",
            },
            "green_snow": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://blocklist.greensnow.co/greensnow.txt",
                "name": "GreenSnow",
            },
            "rjmblocklist_fresh": {
                "list_type": "ip",
                "url": "https://rjmblocklist.com/sizzling/freships.txt",
                "type": "unformatted",
                "name": "RJM Blocklist",
            },
            "rjmblocklist_worst": {
                "list_type": "ip",
                "url": "https://rjmblocklist.com/sizzling/worst.txt",
                "type": "unformatted",
                "name": "RJM Blocklist",
            },
            "openfish": {
                "list_type": "url",
                "url": "https://openphish.com/feed.txt",
                "type": "unformatted",
                "name": "OpenPhish",
            },
            "phishunt.io": {
                "list_type": "url",
                "url": "https://phishunt.io/feed.txt",
                "type": "unformatted",
                "name": "phishunt.io",
            },

            
            # "tweetfeed": { Mukszik meg jo, de csv-t ad vissza nem raw ip cimeket :(
            #     "list_type": "both",
            #     "type": "csv",
            #     "url": "https://raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/today.csv",
            # },
            # "threatlog": {"list_type": "ip", "url": "https://www.threatlog.com/"},
            # "openphish": {"list_type": "ip", "url": "https://openphish.com/"},
            # "nordspam": {"list_type": "ip", "url": "https://www.nordspam.com/"},
            # "azorult_tracker": {
            #     "list_type": "ip",
            #     "url": "https://azorult-tracker.net/doc",
            # },
            # "honeydb": {
            #     "list_type": "ip",
            #     "url": "https://honeydb.io/",
            # },
            # "fspamlist": {
            #     "list_type": "ip",
            #     "url": "http://fspamlist.com/index.php?c=api",
            # },
            # "ipsum": {
            #     "list_type": "ip",
            #     "url": "https://github.com/stamparm/ipsum",
            # },
            # "rjmblocklist": {
            #     "list_type": "ip",
            #     "url": "https://rjmblocklist.com/",
            # },
            # "urlvir": {"list_type": "ip", "url": "https://www.urlvir.com/"},        
        }
        for key, value in source.items():
            self.send_request_and_save_result(
                value["url"], f"{value['list_type']}/{key}.txt", value["list_type"], value["name"]
            )
