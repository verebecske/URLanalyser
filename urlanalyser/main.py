import src.URLAnalyser as URLAnalyser
from flask import Flask, jsonify, request
from logging import Logger, getLogger
from configparser import ConfigParser


class ManagerRob:
    logger: Logger

    def __init__(self):
        self.logger = getLogger()
        set_logger()
        configs = get_config()

    def start_flask(self):
        flaskwrapper = FlaskAppWrapper(logger=self.logger)
        flaskwrapper.run()

    def start_analyser(self):
        safeurl = URLAnalyser(config=self.config["analyser"], logger=self.logger)

    def set_logger(self) -> None:
        pass

    def get_config(self) -> ConfigParser:
        config = ConfigParser()
        config.read("secrets/config.ini")

    def start(self) -> None:
        self.start_analyser()
        self.start_flask()


if __name__ == "__main__":
    rob = ManagerRob()
    rob.start()
