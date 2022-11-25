from configparser import ConfigParser
from src.url_analyser import URLAnalyser
from src.flask.wrapper import FlaskAppWrapper
from src.api_connector import APIConnector
from src.ancestor import Ancestor
from mocks.api_connector import APIConnector as MockConnector
from mocks.url_analyser import URLAnalyser as MockAnalyser


class ManagerRob(Ancestor):
    config: ConfigParser
    debug: bool

    def __init__(self):
        self.get_config()

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
            analyser = MockAnalyser(config=self.config["analyser"], connector=connector)
        else:
            connector = Connector(config=self.config["connector"])
            analyser = Analyser(config=self.config["analyser"], connector=connector)
        self.start_flask(analyser)


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
