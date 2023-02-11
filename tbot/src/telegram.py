import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from src.ancestor import Ancestor
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import re
import requests


class MaliciousContentError(Exception):
    def __str__(self):
        return "Woop-woop someone send something wrong!"


class TBot(Ancestor):
    debug = True
    mytoken: str
    urlanalyser_url: str

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.mytoken = config["token"]
        self.urlanalyser_url = f"http://{config['host']}:{config['port']}"

    def start(self):
        application = ApplicationBuilder().token(self.mytoken).build()

        start_handler = CommandHandler("start", self.start_handler)
        application.add_handler(start_handler)

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo)
        application.add_handler(echo_handler)
        
        url_handler = CommandHandler("url", self.url_handler)
        application.add_handler(url_handler)

        screenshot_handler = CommandHandler("screenshot", self.screenshot_handler)
        application.add_handler(screenshot_handler)

        application.run_polling()

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm not a bot or am I...? Anyway just send me URL",
        )

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        content =  update.message.text
        urls = self.filter_urls(content)
        replay = content
        if len(urls) > 0:
            replay = urls
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=replay
            )

    async def url_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        urls = self.filter_urls(update.message.text)
        res = {}
        for url in urls:
            res[url] = self.inspect_url(url)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=res
        )

    async def screenshot_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm not a bot or am I...? Anyway just send me URL",
        )

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        self.logger.info(f'URLs: {urls}')
        return urls

    def inspect_url(self, url: str) -> bool:
        r = requests.get(f"{self.urlanalyser_url}/check?url={url}")
        return r.json()["result"]

