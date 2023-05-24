from configparser import ConfigParser

from src.ancestor import Ancestor
from src.malaut import Malaut
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskAppWrapper

from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhaus_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.connectors.apivoid_api import APIVoidAPI
from src.connectors.domage_api import DomageAPI
from src.connectors.collector import Collector

from src.database.blocklistdb import BlockListDatabase, BlockListDatabaseFactory

# from mocks.connectors.ipwho_api import IPWhoAPI as MockIPWhoAPI
# from mocks.connectors.urlhaus_api import URLHausAPI as MockURLHausAPI
# from mocks.connectors.virustotal_api import VirusTotalAPI as MockVirusTotalAPI
# from mocks.url_analyser import URLAnalyser as MockAnalyser
# from mocks.malaut import Malaut as MockMalaut


class Application(Ancestor):
    config: ConfigParser
    debug: bool = True

    def __init__(self):
        super().__init__()
        self.get_config()
        self.logger.info("Start URLAnalyser application")

    def get_config(self) -> None:
        self.config = ConfigParser()
        self.config.read("secrets/config.ini")
        self.debug = self.config["urlanalyser"].getboolean("debug")

    def start_flask(self, analyser) -> None:
        flaskwrapper = FlaskAppWrapper(config=self.config["flask"], analyser=analyser)
        flaskwrapper.run()

    def update_static_databases(self, urlhaus_api, collector) -> None:
        urlhaus_api.update_urlhaus_database()
        collector.collect_many()

    def start(self) -> None:
        config = self.config["urlanalyser"]
        urlhaus_api = URLHausAPI(config)
        virustotal_api = VirusTotalAPI(config)
        apivoid_api = APIVoidAPI(config)
        ipwho_api = IPWhoAPI(config)
        malaut = Malaut(config=config)
        domage_api = DomageAPI(config=config)
        blocklistdbfactory = BlockListDatabaseFactory(config)
        blocklistdb = blocklistdbfactory.get_blocklistdb()
        collector = Collector(blocklistdb)
        analyser = URLAnalyser(
            config=config,
            ipwho_api=ipwho_api,
            urlhaus_api=urlhaus_api,
            virustotal_api=virustotal_api,
            apivoid_api=apivoid_api,
            domage_api=domage_api,
            collector=collector,
            malaut=malaut,
        )
        self.update_static_databases(urlhaus_api, collector)
        self.start_flask(analyser)

if __name__ == "__main__":
    app = Application()
    app.start()
