import logging
from configparser import ConfigParser
from src.discord import DBot
from os import getenv


def start_discord(config):
    discord = DBot(config["discord"])
    discord.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    config["discord"]["host"] = getenv("URLANALYSER_HOST")
    config["discord"]["port"] = getenv("URLANALYSER_PORT")
    config["discord"]["debug"] = getenv("DEBUG", True)
    return config


def start():
    config = get_config()
    start_discord(config)


if __name__ == "__main__":
    start()
