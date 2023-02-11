import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from src.ancestor import Ancestor
from src.soul import Soul, MaliciousContentError
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)


class TBot(Ancestor):
    mytoken: str

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.mytoken = config["token"]
        self.tsoul = TelegramClient()

    def start(self):
        application = ApplicationBuilder().token(self.mytoken).build()

        start_handler = CommandHandler("start", self.start_handler)
        application.add_handler(start_handler)

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo)
        application.add_handler(echo_handler)

        application.run_polling()

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm not a bot or am I...? Anyway just send me URL",
        )

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg_dict = {
            "content": update.message.text,
            "author": "not yet",
            "channel": "not yet",
        }
        ans = await self.tsoul.read_direct_message(message=msg_dict)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ans)


class TelegramClient(Soul):
    async def _send_message_to_log_channel(self, message):
        pass

    async def _delete_message(self, message):
        pass

    async def _send_answer(self, message, channel):
        pass

    async def _send_file(self, image, channel):
        pass
