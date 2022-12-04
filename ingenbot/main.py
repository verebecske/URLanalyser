import logging
from configparser import ConfigParser
from src.discord import DBot
from src.telegram import TBot


def start_discord(config):
    discord = DBot(config["discord"])
    discord.start()


def start_telegram(config):
    telegram = TBot(config["telegram"])
    telegram.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    return config


def start():
    config = get_config()
    # start_discord(config)
    start_telegram(config)


if __name__ == "__main__":
    start()
