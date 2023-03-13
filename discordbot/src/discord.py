from discord.ext import tasks, commands
import discord
import time
from src.ancestor import Ancestor
import re
import requests


class MaliciousContentError(Exception):
    def __str__(self):
        return "Woop-woop someone send something wrong!"


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


class DiscordClient(commands.Bot, Ancestor):
    debug = True
    log_channel = None

    async def send_message(self, channel: discord.channel, text):
        print(f"I send: {str(text)}\nin channel: {str(channel)}")
        self.logger("Hello")
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

    async def read_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")
        replay = ""
        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self._send_answer(replay, channel)
        url_list = self.filter_urls(req)
        if self.is_malicious_list(url_list):
            raise MaliciousContentError
        return replay

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        print("URLS:", urls)
        return urls

    def is_malicious_list(self, url_list: list) -> bool:
        is_malicious = False
        for url in url_list:
            is_malicious = is_malicious or self.inspect_url(url)
        print("Results:", is_malicious)
        return is_malicious

    def inspect_url(self, url: str) -> bool:
        host = "urlanalyser-urlanalyser-1"
        port = 5000
        mock_list = ["reallykaros.io", "virus.hu", "virus.com"]
        A = url in mock_list
        r = requests.get(f"http://{host}:{port}/check?url={url}")
        if r.status_code == 200:
            B = r.json()["result"]
        return A or B

    async def read_direct_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")

        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self._send_answer(replay, channel)

        urls = self.filter_urls(req)
        if urls == []:
            replay = "Hey Tom, it's Bob!"
        else:
            replay = await self.send_to_analyser(urls, channel)
        return replay

    async def send_to_analyser(self, urls: list, channel) -> str:
        for url in urls:
            settings = {
                "url": url,
                "urlhaus": True,
                "virustotal": True,
                "geoip": True,
                "history": True,
            }
            answer = self.ask_urlanalyser_api(url, settings)
            print("ANS:", answer)
            await self._send_answer(str(answer), channel)
            # image = self.get_screenshot(url)
            # await self._send_file(image, channel)
        return str(answer)

    def ask_urlanalyser_api(self, url: str, settings: dict) -> dict:
        host = "urlanalyser-urlanalyser-1"
        port = 5000
        r = requests.post(f"http://{host}:{port}/get_infos", json=settings)
        if r.status_code == 200:
            return r.json()["result"]
        return {"result": ""}

    def get_screenshot(self, url: str) -> str:
        host = "urlanalyser-urlanalyser-1"
        port = 5000
        path = "./images/screenshot.png"
        r = requests.get(f"http://{host}:{port}/image?url={url}")
        with open(path, "wb") as image_file:
            image_file.write(r.content)
        return path
