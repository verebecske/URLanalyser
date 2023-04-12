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
        config = {
            "host": "urlanalyser-urlanalyser-1",
            "port": 5000,
        }
        bot.set_urlanalyser(config)
        bot.run(self.mytoken)


class DiscordClient(commands.Bot, Ancestor):
    debug = True
    log_channel = None

    def __init__(self, command_prefix, intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        Ancestor.__init__(self)
        self.logger.info("Start DiscordClient")

    def set_urlanalyser(self, config: dict) -> None:
        self.urlanalyser_url = f"http://{config['host']}:{config['port']}"

    # Discord default

    async def send_message(self, channel: discord.channel, text):
        self.logger.info(f"I send: {str(text)}\nin channel: {str(channel)}")
        if channel is not None:
            await channel.send(text)

    async def on_message_delete(self, message):
        msg = f"{message.author} has deleted the message: {message.content}"
        await self._send_message_to_log_channel(msg)

    async def delete_message(self):
        if message.content.startswith("!deleteme"):
            msg = await message.channel.send("I will delete myself now...")
            await msg.delete()
        if message.content.startswith("!delme"):
            await message.channel.send("Goodbye in 3 seconds...", delete_after=3.0)

    async def on_ready(self):
        self.logger.info("We have logged in as {0.user}".format(self))
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
            answer = await self._read_direct_message(message=msg_dict)
            if answer != "":
                await self._send_answer(answer, message.channel)
        else:
            try:
                answer = await self._read_message(message=msg_dict)
            except MaliciousContentError as e:
                await self._delete_message(message)
                await self._send_answer(e, message.channel)
                return
            if answer != "":
                await self._send_answer(answer, message.channel)

    async def _read_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        self.logger.info(
            f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}"
        )
        replay = ""
        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self._send_answer(replay, channel)
        url_list = self._filter_urls(req)
        if self._is_malicious_list(url_list):
            raise MaliciousContentError
        return replay

    async def _delete_message(self, message):
        await message.delete()

    async def _send_answer(self, message, channel):
        while len(message) > 2000:
            await channel.send(message[:2000])
            message = message[2000:]
        await channel.send(message)

    async def _send_message_to_log_channel(self, msg):
        if self.log_channel is None:
            self._set_log_channel()
        await self.log_channel.send(msg)

    def _set_log_channel(self):
        for channel in self.get_all_channels():
            if channel.guild == "IngenServer" and channel.name == "log-ingenbot":
                break
        self.log_channel = channel

    def _filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        self.logger.info(f"URLS: {urls}")
        return urls

    def _is_malicious_list(self, url_list: list) -> bool:
        is_malicious = False
        for url in url_list:
            is_malicious = is_malicious or self._inspect_url(url)
        self.logger.info(f"Results: {is_malicious}")
        return is_malicious

    def _inspect_url(self, url: str) -> bool:
        url = self._encode_url(url)
        response = requests.get(f"{self.urlanalyser_url}/check?url={url}")
        try:
            if response.status_code == 200:
                return response.json()["result"]["is_malicious"]
        except Exception as erroir:
            self.logger.error(f"Error happened: {error}")
        return False

    async def _read_direct_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        self.logger.info(
            f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}"
        )
        if self.debug:
            replay = f"**{user}** sent me:\n\t{req}"
            await self._send_answer(replay, channel)
        urls = self._filter_urls(req)
        if urls == []:
            replay = "Missing URL"
        else:
            replay = await self._send_to_analyser(urls, channel)
        return replay

    async def _send_to_analyser(self, urls: list, channel) -> str:
        for url in urls:
            settings = {
                "url": url,
                "urlhaus": True,
                "virustotal": True,
                "geoip": True,
                "history": True,
            }
            answer = self._ask_urlanalyser_api(url, settings)
            for key in answer.keys():
                result = str(answer[key])
                await self._send_answer(f"**{key}**: {result}", channel)
            image = self._get_screenshot(url)
            await self._send_file(image, channel)
        return str(answer)

    def _ask_urlanalyser_api(self, url: str, settings: dict) -> dict:
        try:
            response = requests.post(f"{self.urlanalyser_url}/get_infos", json=settings)
            if response.status_code == 200:
                return response.json()["result"]
            else:
                return f"Error happened with url: {url} - status code: {response.status_code}"
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            return {"result": ""}

    def _get_screenshot(self, url: str) -> str:
        url = self._encode_url(url)
        path = "./images/screenshot.png"
        response = requests.get(f"{self.urlanalyser_url}/get_screenshot?url={url}")
        with open(path, "wb") as image_file:
            image_file.write(response.content)
        return path

    async def _send_file(self, path, channel):
        path = "./images/screenshot.png"
        with open(path, "rb") as file:
            discord_file = discord.File(file, filename=path)
        await channel.send(file=discord_file)

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()
