from src.ancestor import Ancestor
import requests
import ipaddress
from collections import defaultdict


class Collector(Ancestor):
    def __init__(self):
        super().__init__()
        self.in_memory_bad_ips = defaultdict(list)
        self.in_memory_bad_urls = defaultdict(list)

    def send_request_and_save_result(self, url, filename, list_type):
        response = requests.get(url=url)
        with open(f"static_database/{filename}", "w") as fd:
            fd.write(response.text)
        for line in response.text.split("\n"):
            if line.startswith("#"): 
                continue
            line.strip()
            try:
                if list_type == "ip":
                    ip = ipaddress.ip_address(line)
                    self.in_memory_bad_ips[ip].append(filename)
                if list_type == "url":
                    self.in_memory_bad_urls[line].append(filename)
            except ValueError as error:
                self.logger.warning(f"line: {line} error {error}")

    def collect_many(self):
        source = {
            "mirai": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://mirai.security.gives/data/ip_list.txt",
                "name": "",
            },
            "nubi_network": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://www.nubi-network.com/list.txt",
            },
            "liquidbinary": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://liquidbinary.com/blackIPs.txt",
            },
            "sigs_interserver": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://sigs.interserver.net/iprbl.txt",
            },
            "blisxfr": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://bl.isx.fr/raw",
            },
            "blacklists": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "http://blacklists.co/download/all.txt",
            },
            "threat sourcing": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://www.threatsourcing.com/ipall.txt",
            },
            "feodo": {
                "list_type": "ip",
                "name": "https://feodotracker.abuse.ch/blocklist/#ip-blocklist",
                "type": "unformatted",
                "url": "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt",
            },
            "charles_haleys": {
                "list_type": "ip",
                "type": "unformatted",
                "url": "https://charles.the-haleys.org/ssh_dico_attack_with_timestamps.php?days=1",
            },
            "green_snow": {
                "list_type": "ip",
                "name": "https://greensnow.co/",
                "type": "unformatted",
                "url": "https://blocklist.greensnow.co/greensnow.txt",
            },
            "rjmblocklist_fresh": {
                "list_type": "ip",
                "name": "https://rjmblocklist.com/",
                "url": "https://rjmblocklist.com/sizzling/freships.txt",
                "type": "unformatted",
            },
            "rjmblocklist_worst": {
                "list_type": "ip",
                "name": "https://rjmblocklist.com/",
                "url": "https://rjmblocklist.com/sizzling/worst.txt",
                "type": "unformatted",
            },
            "openfish": {
                "list_type": "url",
                "name": "openfish",
                "url": "https://openphish.com/feed.txt",
                "type": "unformatted",
            }
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
                value["url"], f"{value['list_type']}/{key}.txt", value["list_type"]
            )

    def check_ip_reputation(self, ip: str) -> list:
        ip_addr = ipaddress.ip_address(ip)
        return self.in_memory_bad_ips.get(ip_addr, [])

    def check_url_reputation(self, url: str) -> list:
        return self.in_memory_bad_urls.get(url, [])

    def get_is_malicous_result(self, ip, url) -> bool:
        return self.check_ip_reputation(ip) != [] or self.check_url_reputation(url) != []