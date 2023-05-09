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

        check_url_handler = CommandHandler("check", self.check_url_handler)
        application.add_handler(check_url_handler)

        screenshot_handler = CommandHandler("screenshot", self.screenshot_handler)
        application.add_handler(screenshot_handler)

        virustotal_handler = CommandHandler("virustotal", self.virustotal_handler)
        application.add_handler(virustotal_handler)

        urlhaus_handler = CommandHandler("urlhaus", self.urlhaus_handler)
        application.add_handler(urlhaus_handler)

        location_handler = CommandHandler("location", self.location_handler)
        application.add_handler(location_handler)

        domain_age_handler = CommandHandler("domain_age", self.domain_age_handler)
        application.add_handler(domain_age_handler)

        domain_reputation_handler = CommandHandler(
            "domain_reputation", self.domain_reputation_handler
        )
        application.add_handler(domain_reputation_handler)

        download_as_zip_handler = CommandHandler(
            "download", self.download_as_zip_handler
        )
        application.add_handler(download_as_zip_handler)

        history_handler = CommandHandler("history", self.history_handler)
        application.add_handler(history_handler)

        index_handler = CommandHandler("index", self.index_handler)
        application.add_handler(index_handler)

        help_handler = CommandHandler("help", self.help_handler)
        application.add_handler(help_handler)

        application.run_polling()

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Send me an URL, and use /help if you need some help",
        )

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        content = update.message.text
        urls = self.filter_urls(content)
        replay = content
        if len(urls) > 0:
            replay = urls
        await context.bot.send_message(chat_id=update.effective_chat.id, text=replay)

    async def check_url_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            await self.send_request_and_answer("check", url, update, context)

    async def send_request_and_answer(
        self,
        endpoint: str,
        url: str,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        try:
            response = requests.get(
                f"{self.urlanalyser_url}/{endpoint}?url={self._encode_url(url)}"
            )
            if response.status_code == 200:
                answer = self._format_dict_answer(response.json())
            else:
                answer = f"Something went wrong with: {url} - status code: {response.status_code}"
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=answer,
            )
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Error happend while processing {url} - please send your message again",
            )

    async def location_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            await self.send_request_and_answer("get_location", url, update, context)

    async def domain_age_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            await self.send_request_and_answer("get_domain_age", url, update, context)

    async def domain_reputation_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            await self.send_request_and_answer(
                "get_domain_reputation", url, update, context
            )

    async def download_as_zip_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            await self.send_request_and_answer("download_as_zip", url, update, context)

    async def virustotal_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        settings = {
            "urlhaus": False,
            "virustotal": True,
            "location": False,
            "history": False,
        }
        await self.collect_urls_and_send_get_infos(
            message=update.message.text,
            settings=settings,
            update=update,
            context=context,
        )

    async def urlhaus_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = {
            "urlhaus": True,
            "virustotal": False,
            "location": False,
            "history": False,
        }
        await self.collect_urls_and_send_get_infos(
            message=update.message.text,
            settings=settings,
            update=update,
            context=context,
        )

    async def _location_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        settings = {
            "urlhaus": False,
            "virustotal": False,
            "location": True,
            "history": False,
        }
        await self.collect_urls_and_send_get_infos(
            message=update.message.text,
            settings=settings,
            update=update,
            context=context,
        )

    async def history_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = {
            "urlhaus": False,
            "virustotal": False,
            "location": False,
            "history": True,
        }
        await self.collect_urls_and_send_get_infos(
            message=update.message.text,
            settings=settings,
            update=update,
            context=context,
        )

    async def collect_urls_and_send_get_infos(
        self,
        message: str,
        settings: dict,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        urls = self.filter_urls(message)
        if len(urls) == 0:
            raise ValueError("Missing URL")
        for url in urls:
            try:
                settings["url"] = url
                response = requests.post(
                    f"{self.urlanalyser_url}/get_infos", json=settings
                )
                if response.status_code == 200:
                    answer = self._format_dict_answer(response.json())
                else:
                    answer = f"Something went wrong with: {url} - status code: {response.status_code}"
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=answer,
                )
            except Exception as error:
                self.logger.error(f"Error happened: {error}")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Error happend while processing {url} - please send your message again",
                )

    async def index_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            response = requests.get(f"{self.urlanalyser_url}")
            if response.status_code == 200:
                answer = response.json()["message"]
        except Exception as error:
            answer = "Something went wrong"
            self.logger.error(f"Error happened: {error}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

    async def screenshot_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        urls = self.filter_urls(update.message.text)
        if len(urls) == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Missing URL"
            )
            return
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Taking screenshot can be slow - thank for your patience",
        )
        for url in urls:
            url = self._encode_url(url)
            response = requests.get(f"{self.urlanalyser_url}/get_screenshot?url={url}")
            if response.status_code == 200:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=response.content
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Something went wrong with: {url}",
                )

    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_message = (
            "*Commands:*\n\n"
            + "/help \- send this text\n"
            + "/start \- answer a text\n"
            + "/index \- test message to urlanalyser\n"
            + "/screenshot <url\> \- create a screenshot about the webpage and send it back\n"
            + "/check <url\> \- just a quick test about the url \n"
            + "/virustotal <url\> \- send url to virustotal \n"
            + "/urlhaus <url\> \- send url to urlhaus \n"
            + "/location <url\> \- send url to location \n"
            + "/domain\_age <url\> \- send url to domain age \n"
            + "/domain\_reputation <url\> \- send url to domain age \n"
            + "/download <url\> \- download as zip \n"
            + "/history <url\> \- get url redirect path \n"
            + "\n_If you have any question ask:_\n"
            + "[my creator](https://t.me/trulr)"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=help_message,
            parse_mode="MarkdownV2",
        )

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        self.logger.info(f"URLs: {urls}")
        return urls

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()

    def _format_dict_answer(self, result: dict) -> str:
        text = ""
        for key, value in result.items():
            text += f"**{key}**: {value}\n"
        return text