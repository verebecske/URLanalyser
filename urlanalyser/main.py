from src.url_analyser import URLAnalyser
from src.flask.app_wrapper import FlaskAppWrapper
from src.api_connector import APIConnector
from logging import Logger, getLogger, DEBUG
from configparser import ConfigParser


class ManagerRob:
    logger: Logger
    config: ConfigParser

    def __init__(self):
        self.logger = getLogger()
        self.set_logger()
        self.get_config()

    def start_flask(self, analyser) -> None:
        config = self.config["flask"]
        flaskwrapper = FlaskAppWrapper(
            config=config, analyser=analyser, logger=self.logger
        )
        flaskwrapper.run()

    def get_connector(self) -> APIConnector:
        config = self.config["connector"]
        connector = APIConnector(config=config, logger=self.logger)
        return connector

    def get_analyser(self, connector: APIConnector) -> URLAnalyser:
        config = self.config["analyser"]
        analyser = URLAnalyser(config=config, connector=connector, logger=self.logger)
        return analyser

    def set_logger(self) -> None:
        self.logger.setLevel(DEBUG)
        self.logger.error("Start")

    def get_config(self) -> None:
        self.config = ConfigParser()
        self.config.read("secrets/config.ini")

    def start(self) -> None:
        connector = self.get_connector()
        analyser = self.get_analyser(connector)
        self.start_flask(analyser)


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
