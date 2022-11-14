import logging
from src.discord import DBot
from configparser import ConfigParser


def get_logger():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    return logger


def start_discord():
    config = get_config()
    logger = get_logger()
    discord = DBot(config["discord"], logger)
    discord.start()


def get_config():
    config = ConfigParser()
    config.read("secrets/config.ini")
    return config


if __name__ == "__main__":

    start_discord()
