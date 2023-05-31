from configparser import ConfigParser
from src.telegram import TBot
from os import getenv


def start_telegram(config):
    telegram = TBot(config["telegram"])
    telegram.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    config["telegram"]["host"] = getenv("URLANALYSER_HOST")
    config["telegram"]["port"] = getenv("URLANALYSER_PORT")
    config["telegram"]["debug"] = getenv("DEBUG", True)
    return config


def start():
    config = get_config()
    start_telegram(config)


if __name__ == "__main__":
    start()
