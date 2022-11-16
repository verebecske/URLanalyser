from discord.ext import tasks, commands
import discord
from logging import Logger
from src.soul import Soul


class DBot:
    mytoken: str
    logger: Logger
    intents: discord.Intents

    def __init__(self, config: dict, logger: Logger) -> None:
        self.logger = logger
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
        bot = DiscordClient(command_prefix="", intents=self.intents)
        bot.run(self.mytoken)


class DiscordClient(commands.Bot, Soul):
    async def send_message(self, channel: discord.channel, text):
        print(f"I send: {str(text)}\nin channel: {str(channel)}")
        if channel is not None:
            await channel.send(text)

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg_dict = {
            "content": message.content,
            "author": message.author,
            "channel": message.channel,
        }
        print("HEY: ", message.channel.type)
        if message.channel.type == discord.ChannelType.private:
            answer = await self.read_direct_message(message=msg_dict)
            await self.send_answer(answer, message.channel)
        else:
            answer = await self.read_message(message=msg_dict)
            if answer != "":
                await self.send_answer(answer, message.channel)

    async def send_answer(self, message, channel):
        await channel.send(message)
