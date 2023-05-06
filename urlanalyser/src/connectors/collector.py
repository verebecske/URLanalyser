from ancestor import Ancestor


class Collector(Ancestor):

    def get_blacklists_all(self):
        response = requests.get(url="http://blacklists.co/download/all.txt")
        with open("static_database/urlhaus/blacklists_co_all.txt", "w") as fd:
            fd.write(response.text)
        self.logger.info("Blacklists.co database updated")

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

    def get_gpf_dns_block_list(self): # maybe not
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