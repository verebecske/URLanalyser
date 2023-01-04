from configparser import ConfigParser
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskAppWrapper
from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhause_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.ancestor import Ancestor
from src.malaut import Malaut
from mocks.connectors.ipwho_api import IPWhoAPI as MockIPWhoAPI
from mocks.connectors.urlhause_api import URLHausAPI as MockURLHausAPI
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

    def start(self) -> None:
        if self.debug:
            connector = MockConnector(config=self.config["connector"])
            malaut = MockMalaut(config=self.config["malaut"])
            analyser = MockAnalyser(
                config=self.config["analyser"], connector=connector, malaut=malaut
            )
        else:
            urlhause_api = URLHausAPI(config["urlhaus"])
            virustotal_api = VirusTotalAPI(config["virustotal"])
            ipwhois = IPWhoAPI(config)

            malaut = Malaut(config=self.config["malaut"])
            analyser = URLAnalyser(
                config=self.config["analyser"], connector=connector, malaut=malaut
            )
        self.start_flask(analyser)


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
