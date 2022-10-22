import src.URLAnalyser as URLAnalyser
from flask import Flask, jsonify, request
from logging import Logger, getLogger


def start_flask(logger: Logger):
    flaskwrapper = FlaskAppWrapper(logger=logger)
    flaskwrapper.run()


if __name__ == "__main__":
    logger = logging.getLogger()
    safeurl = URLAnalyser({}, logger=logger)
    url = "https://urlhaus-api.abuse.ch/"
    # url = "http://113.88.209.132:42715/i"
    ans = safeurl.dummy_is_malware(url)
