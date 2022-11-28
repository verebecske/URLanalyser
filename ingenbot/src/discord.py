from discord.ext import tasks, commands
import discord
from logging import Logger
from src.soul import Soul, MaliciousContentError
from src.ancestor import Ancestor
import time


class DBot(Ancestor):
    mytoken: str
    intents: discord.Intents

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.mytoken = config["token"]

    def set_intents(self) -> None:
        self.logger.info("Set discord client")
        intents = discord.Intents.default()
        intents.typing = True
        intents.members = True
        intents.message_content = True
        intents.dm_typing = True
        intents.dm_reactions = True
        intents.dm_messages = True
        self.intents = intents

    def start(self):
        self.set_intents()
        bot = DiscordClient(
            command_prefix="",
            intents=self.intents,
        )
        bot.run(self.mytoken)


class DiscordClient(commands.Bot, Soul):
    log_channel = None

    async def send_message(self, channel: discord.channel, text):
        print(f"I send: {str(text)}\nin channel: {str(channel)}")
        if channel is not None:
            await channel.send(text)

    async def _delete_message(self, message):
        await message.delete()

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))
        self._set_log_channel()

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg_dict = {
            "content": message.content,
            "author": message.author,
            "channel": message.channel,
        }
        if message.channel.type == discord.ChannelType.private:
            answer = await self.read_direct_message(message=msg_dict)
            if answer != "":
                await self._send_answer(answer, message.channel)
        else:
            try:
                answer = await self.read_message(message=msg_dict)
            except MaliciousContentError as e:
                await self._delete_message(message)
                await self._send_answer(e, message.channel)
                return
            if answer != "":
                await self._send_answer(answer, message.channel)

    async def _send_answer(self, message, channel):
        await channel.send(message)

    async def on_message_delete(self, message):
        msg = f"{message.author} has deleted the message: {message.content}"
        await self._send_message_to_log_channel(msg)

    async def delete_message(self):
        if message.content.startswith("!deleteme"):
            msg = await message.channel.send("I will delete myself now...")
            await msg.delete()

        if message.content.startswith("!delme"):
            await message.channel.send("Goodbye in 3 seconds...", delete_after=3.0)

    async def _send_message_to_log_channel(self, msg):
        if self.log_channel is None:
            self._set_log_channel()
        await self.log_channel.send(msg)

    def _set_log_channel(self):
        for channel in self.get_all_channels():
            if channel.guild == "IngenServer" and channel.name == "log-ingenbot":
                break
        self.log_channel = channel

    async def _send_file(self, path, channel):
        path = "./images/screenshot.png"
        with open(path, "rb") as fh:
            f = discord.File(fh, filename=path)
        await channel.send(file=f)
