import logging
from configparser import ConfigParser
from src.discord import DBot


def start_discord():
    config = get_config()
    discord = DBot(config["discord"])
    discord.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    return config


if __name__ == "__main__":
    start_discord()
