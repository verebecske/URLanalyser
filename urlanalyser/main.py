from threading import Thread
import os, time
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

        self.config["urlanalyser"]["debug"] = os.getenv("DEBUG", True)
        self.config["urlanalyser"]["update_delay"] = os.getenv("UPDATE_DELAY", "300")
        self.config["urlanalyser"]["redis_host"] = os.getenv("REDIS_HOST", None)
        self.config["urlanalyser"]["selenium_host"] = os.getenv("SELENIUM_HOST", "selenium-hub")
        self.config["urlanalyser"]["selenium_post"] = os.getenv("SELENIUM_PORT", "4444")
        self.debug = self.config["urlanalyser"]

        self.config["flask"]["debug"] = os.getenv("DEBUG", True)
        self.config["flask"]["host"] = os.getenv("FLASK_HORT", "0.0.0.0")
        self.config["flask"]["port"] = os.getenv("FLASK_PORT", "5000")


    def start_flask(self, analyser) -> None:
        flaskwrapper = FlaskWrapper(config=self.config["flask"], analyser=analyser)
        flaskwrapper.run()

    def update_static_databases(self, delay) -> None:
        while True:
            self.urlhaus_api.update_urlhaus_database()
            self.collector.collect_many()
            time.sleep(int(delay))

    def start(self) -> None:
        config = self.config["urlanalyser"]
        self.urlhaus_api = URLHausAPI(config)
        virustotal_api = VirusTotalAPI(config)
        apivoid_api = APIVoidAPI(config)
        ipwho_api = IPWhoAPI(config)
        sample_analyser = SampleAnalyser(config=config)
        domage_api = DomageAPI(config=config)
        blocklistdbfactory = BlockListDatabaseFactory(config)
        blocklistdb = blocklistdbfactory.get_blocklistdb()
        self.collector = Collector(blocklistdb)
        analyser = URLAnalyser(
            config=config,
            ipwho_api=ipwho_api,
            urlhaus_api=self.urlhaus_api,
            virustotal_api=virustotal_api,
            apivoid_api=apivoid_api,
            domage_api=domage_api,
            collector=self.collector,
            sample_analyser=sample_analyser,
        )
        thread = Thread(
            target=self.update_static_databases, args=(config["update_delay"],)
        )
        thread.start()
        self.start_flask(analyser)
        thread.stop()


if __name__ == "__main__":
    app = Application()
    app.start()
