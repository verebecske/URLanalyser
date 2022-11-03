from logging import Logger, getLogger, DEBUG
from configparser import ConfigParser
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskAppWrapper
from src.api_connector import APIConnector
from mocks.api_connector import APIConnector as MockConnector
from mocks.url_analyser import URLAnalyser as MockAnalyser


class ManagerRob:
    logger: Logger
    config: ConfigParser
    debug: bool

    def __init__(self):
        self.logger = getLogger()
        self.set_logger()
        self.get_config()

    def get_config(self) -> None:
        self.config = ConfigParser()
        self.config.read("secrets/config.ini")
        self.debug = self.config["all"].getboolean("debug")

    def start_flask(self, analyser) -> None:
        config = self.config["flask"]
        flaskwrapper = FlaskAppWrapper(
            config=config, logger=self.logger, analyser=analyser
        )
        flaskwrapper.run()

    def get_connector(self) -> APIConnector:
        config = self.config["connector"]
        connector = APIConnector(config=config, logger=self.logger)
        return connector

    def get_analyser(self, connector: APIConnector) -> URLAnalyser:
        config = self.config["analyser"]
        analyser = URLAnalyser(config=config, logger=self.logger, connector=connector)
        return analyser

    def set_logger(self) -> None:
        self.logger.setLevel(DEBUG)
        self.logger.error("Start")

    def start(self) -> None:
        if self.debug:
            connector = MockConnector(
                config=self.config["connector"], logger=self.logger
            )
            analyser = MockAnalyser(
                config=self.config["analyser"], logger=self.logger, connector=connector
            )
        else:
            connector = self.get_connector()
            analyser = self.get_analyser(connector)
        self.start_flask(analyser)


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
