from discord.ext import tasks, commands
import discord
from logging import Logger


async def send_answer(channel: discord.channel, text):
    print(f"I send: {str(text)}\nin channel: {str(channel)}")
    await channel.send(text)


async def logic_on_message(message):
    req: str = message["content"]
    user: str = message["author"]
    channel = message["channel"]
    print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")

    replay = f"Ezt küldted **{user}**:\n\t{req}"

    if replay != "" and replay is not None:
        await send_answer(channel, replay)


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
        self.intents = intents

    def start(self):
        self.set_intents()
        bot = DiscordClient(command_prefix="", intents=self.intents)
        bot.run(self.mytoken)


class DiscordClient(commands.Bot):
    async def send_message(self, channel: discord.channel, text):
        print(f"I send: {str(text)}\nin channel: {str(channel)}")
        if channel is not None:
            await channel.send(text)

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    async def on_message(self, message):
        print(f"I got: {message}\n")
        if message.author == self.user:
            return
        msg_dict = {
            "content": message.content,
            "author": message.author,
            "channel": message.channel,
        }
        await logic_on_message(message=msg_dict)
