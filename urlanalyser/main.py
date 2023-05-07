from configparser import ConfigParser
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskAppWrapper
from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhaus_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.connectors.ipvoid_api import IPVoidAPI
from src.connectors.domage_api import DomageAPI
from src.ancestor import Ancestor
from src.malaut import Malaut
from src.connectors.redis_database import RedisDatabase

from mocks.connectors.ipwho_api import IPWhoAPI as MockIPWhoAPI
from mocks.connectors.urlhaus_api import URLHausAPI as MockURLHausAPI
from mocks.connectors.virustotal_api import VirusTotalAPI as MockVirusTotalAPI
from mocks.url_analyser import URLAnalyser as MockAnalyser
from mocks.malaut import Malaut as MockMalaut


class ManagerRob(Ancestor):
    config: ConfigParser
    debug: bool = True

    def __init__(self):
        super().__init__()
        self.get_config()
        self.logger.info("Start URLAnalyser application")

    def get_config(self) -> None:
        self.config = ConfigParser()
        self.config.read("secrets/config.ini")
        self.debug = self.config["all"].getboolean("debug")

    def start_flask(self, analyser) -> None:
        config = self.config["flask"]
        flaskwrapper = FlaskAppWrapper(config=config, analyser=analyser)
        flaskwrapper.run()

    def update_static_databases(self, urlhaus_api) -> None:
        urlhaus_api.update_urlhaus_database()
        collector.get_blacklists_all()

    def start(self) -> None:
        config = self.config
        if self.debug:
            malaut = MockMalaut(config=self.config["malaut"])
            urlhaus_api = MockURLHausAPI(config["urlhaus"])
            virustotal_api = MockVirusTotalAPI(config["virustotal"])
            ipwho_api = MockIPWhoAPI(config)
            redis = RedisDatabase(config["redis"])
            domage_api = DomageAPI({})
            analyser = MockAnalyser(
                config=self.config["analyser"],
                ipwho_api=ipwho_api,
                urlhaus_api=urlhaus_api,
                virustotal_api=virustotal_api,
                malaut=malaut,
                domage_api=domage_api,
                redis=redis,
            )
        else:
            urlhaus_api = URLHausAPI(config["urlhaus"])
            virustotal_api = VirusTotalAPI(config["virustotal"])
            ipvoid_api = IPVoidAPI(config["ipvoid"])
            ipwho_api = IPWhoAPI(config)
            malaut = Malaut(config=self.config["malaut"])
            domage_api = DomageAPI({})
            redis = RedisDatabase(config["redis"])
            analyser = URLAnalyser(
                config=self.config["analyser"],
                ipwho_api=ipwho_api,
                urlhaus_api=urlhaus_api,
                virustotal_api=virustotal_api,
                ipvoid_api=ipvoid_api,
                domage_api=domage_api,
                malaut=malaut,
                redis=redis,
            )
        self.start_flask(analyser)


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
