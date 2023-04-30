import logging
from configparser import ConfigParser
from src.discord import DBot


def start_discord(config):
    discord = DBot(config["discord"])
    discord.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    return config


def start():
    config = get_config()
    start_discord(config)


if __name__ == "__main__":
    start()
