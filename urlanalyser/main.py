from configparser import ConfigParser

from src.ancestor import Ancestor
from src.sample_analyser import SampleAnalyser
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskWrapper

from src.connectors.ipwho_api import IPWhoAPI
from src.connectors.urlhaus_api import URLHausAPI
from src.connectors.virustotal_api import VirusTotalAPI
from src.connectors.apivoid_api import APIVoidAPI
from src.connectors.domage_api import DomageAPI
from src.connectors.collector import Collector

from src.database.blocklistdb import BlockListDatabase, BlockListDatabaseFactory


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
        flaskwrapper = FlaskWrapper(config=self.config["flask"], analyser=analyser)
        flaskwrapper.run()

    def update_static_databases(self, urlhaus_api, collector) -> None:
        urlhaus_api.update_urlhaus_database()
        collector.collect_many()
        # TODO: adj hozzá egy időzítőt hogy frissítse magát,
        # és a milyen időnként konfigurálható legyen

    def start(self) -> None:
        config = self.config["urlanalyser"]
        urlhaus_api = URLHausAPI(config)
        virustotal_api = VirusTotalAPI(config)
        apivoid_api = APIVoidAPI(config)
        ipwho_api = IPWhoAPI(config)
        sample_analyser = SampleAnalyser(config=config)
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
            sample_analyser=sample_analyser,
        )
        self.update_static_databases(urlhaus_api, collector)
        self.start_flask(analyser)


if __name__ == "__main__":
    app = Application()
    app.start()
