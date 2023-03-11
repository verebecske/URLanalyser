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
import base64


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

        sr_handler = CommandHandler("sr", self.screenshot_handler)
        application.add_handler(sr_handler)

        vt_handler = CommandHandler("vt", self.virustotal_handler)
        application.add_handler(vt_handler)

        uh_handler = CommandHandler("uh", self.urlhaus_handler)
        application.add_handler(uh_handler)

        gi_handler = CommandHandler("gi", self.geoip_handler)
        application.add_handler(gi_handler)

        hi_handler = CommandHandler("hi", self.history_handler)
        application.add_handler(hi_handler)

        index_handler = CommandHandler("index", self.index_handler)
        application.add_handler(index_handler)

        help_handler = CommandHandler("help", self.help_handler)
        application.add_handler(help_handler)

        application.run_polling()

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm not a bot or am I...? Anyway just send me an URL",
        )

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        content = update.message.text
        urls = self.filter_urls(content)
        replay = content
        if len(urls) > 0:
            replay = urls
        await context.bot.send_message(chat_id=update.effective_chat.id, text=replay)

    async def url_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        urls = self.filter_urls(update.message.text)
        res = {}
        if len(urls) == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Missing the URL"
            )
        for url in urls:
            result = self.inspect_url(url)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=result
            )

    async def virustotal_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        settings = {
            "urlhaus": False,
            "virustotal": True,
            "geoip": False,
            "history": False,
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.send_get_infos(pdate.message.text, settings),
        )

    async def urlhaus_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = {
            "urlhaus": True,
            "virustotal": False,
            "geoip": False,
            "history": False,
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.send_get_infos(pdate.message.text, settings),
        )

    async def geoip_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = {
            "urlhaus": False,
            "virustotal": False,
            "geoip": True,
            "history": False,
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.send_get_infos(pdate.message.text, settings),
        )

    async def geoip_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = {
            "urlhaus": False,
            "virustotal": False,
            "geoip": False,
            "history": True,
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.send_get_infos(pdate.message.text, settings),
        )

    async def send_get_infos(self, message: str, settings: dict) -> str:
        urls = self.filter_urls(message)
        if len(urls) == 0:
            return "Missing URL"
        for url in urls:
            settings["url"] = url
            answer = f"Something went wrong with: {url}"
            r = requests.post(f"{self.urlanalyser_url}/get_infos", json=settings)
            if r.status_code == 200:
                answer = r.json()
            return answer

    async def index_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        r = requests.get(f"{self.urlanalyser_url}")
        answer = "Something went wrong"
        if r.status_code == 200:
            answer = r.json()["message"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

    async def screenshot_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        urls = self.filter_urls(update.message.text)
        if len(urls) == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Missing URL"
            )
        for url in urls:
            url = self._encode_url(url)
            r = requests.get(f"{self.urlanalyser_url}/image?url={url}")
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=r.content
            )

    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_message = (
            "*Commands:*\n"
            + "/help - send this text\n"
            + "/start - answer a text\n"
            + "/index - test message to urlanalyser\n"
            + "/url [url] - inspect url\n"
            + "/screenshot [url] - create a screenshot about the webpage and send it back\n"
            + "/check [url] - just a quick test about the url \n"
            + "/sr [url] - same as /screenshot use it, if you lazy\n"
            + "/vt [url] - send url to virustotal \n"
            + "/uh [url] - send url to urlhaus \n"
            + "/gi [url] - send url to geoip \n"
            + "/hi [url] - get url redirect path \n"
            + "\n_If you have any question ask:_\n"
            + "[my creater](https://t.me/trulr)"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=help_message,
            parse_mode="markdown",
        )

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        self.logger.info(f"URLs: {urls}")
        return urls

    def inspect_url(self, url: str) -> bool:
        url = self._encode_url(url)
        r = requests.get(f"{self.urlanalyser_url}/check?url={url}")
        if r.status_code == 200:
            return r.json()["result"]
        else:
            return r.json()["error"]

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()
