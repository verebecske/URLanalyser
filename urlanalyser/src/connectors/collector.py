from ancestor import Ancestor


class Collector(Ancestor):
    def send_request_and_save_result(self, url, filename):
        response = requests.get(url=url)
        with open("static_database/{filename}", "w") as fd:
            fd.write(response.text)
        self.logger.info("{filename} database updated")

    def get_blacklists_all(self):
        url = "http://blacklists.co/download/all.txt"
        filename = "blacklist_co.txt"
        self.send_request_and_save_result(url, filename)

    def get_azorult_tracker(self):
        pass
        # https://azorult-tracker.net/doc

    def get_charles_haleys(self):
        pass
        # https://charles.the-haleys.org/ssh_dico_attack_with_timestamps.php?days=1

    def get_darklist_de(self):
        pass
        # https://www.darklist.de/

    def get_honey_db(self):
        pass
        # https://honeydb.io/

    def get_green_snow(self):
        pass
        # https://greensnow.co/

    def get_gpf_dns_block_list(self):  # maybe not
        pass
        # https://www.gpf-comics.com/dnsbl/export.php

    def get_feodo(self):
        pass
        # https://feodotracker.abuse.ch/blocklist/#ip-blocklist
        # a kedvenc svajciaim

    def get_fspamlist(self):
        pass
        # http://fspamlist.com/index.php?c=api

    def get_ipsum(self):
        pass
        # https://github.com/stamparm/ipsum
        # ez eleg kiraly

    def get_rim(self):
        pass
        # https://rjmblocklist.com/

    def collect_many(self):
        source = {
            "urlvir": "https://www.urlvir.com/",
            "tweetfeed": "https://github.com/0xDanielLopez/TweetFeed",
            "threatlog": "https://www.threatlog.com/",
            "threat sourcing": "https://www.threatsourcing.com/",
            "openphish": "https://openphish.com/",
            "nordspam": "https://www.nordspam.com/",
            "mirai": "https://mirai.security.gives/data/ip_list.txt",
            "nubi_network": "https://www.nubi-network.com/list.txt",
            "liquidbinary": "http://liquidbinary.com/blackIPs.txt",
            "sigs_interserver": "http://sigs.interserver.net/iprbl.txt",
            "blisxfr": "https://bl.isx.fr/raw",
        }
