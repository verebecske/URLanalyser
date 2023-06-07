from configparser import ConfigParser
from src.discord import DBot
from os import getenv


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    config["discord"]["urlanalyser_host"] = getenv("URLANALYSER_HOST", "urlanalyser")
    config["discord"]["urlanalyser_port"] = getenv("URLANALYSER_PORT", 5000)
    config["discord"]["debug"] = getenv("DEBUG", "true")
    return config


def start():
    config = get_config()
    discord = DBot(config["discord"])
    discord.start()


if __name__ == "__main__":
    start()
