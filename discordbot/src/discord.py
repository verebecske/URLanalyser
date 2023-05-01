from discord.ext import tasks, commands
import discord
import time
from src.ancestor import Ancestor
import re
import requests
import base64
import io


class MaliciousContentError(Exception):
    def __str__(self):
        return "Woop-woop someone send something wrong!"


class DBot(Ancestor):
    mytoken: str
    intents: discord.Intents

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.mytoken = config["token"]
        if "urlanlayser_host" in config:
            self.urlanlayser_host = config["urlanlayser_host"]
        else:
            self.urlanlayser_host = "urlanalyser-urlanalyser-1"
        if "urlanalyser_port" in config:
            self.urlanlayser_port = config["urlanalyser_port"]
        else:
            self.urlanlayser_port = 5000

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
            "host": self.urlanlayser_host,
            "port": self.urlanlayser_port,
        }
        bot.set_urlanalyser(config)
        bot.run(self.mytoken)


class DiscordClient(commands.Bot, Ancestor):
    debug = False
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
        response = requests.get(
            f"{self.urlanalyser_url}/check?url={self._encode_url(url)}"
        )
        try:
            if response.status_code == 200:
                return response.json()["result"]["is_malicious"]
        except Exception as erroir:
            self.logger.error(f"Error happened: {error}")
        return False

    def _set_helper_text(self) -> str:
        help_message = (
            "**Commands:**\n\n"
            + "!help - send this text\n"
            + "!index - test message to urlanalyser\n"
            + "!url [url] - inspect url\n"
            + "!screenshot [url] - create a screenshot about the webpage and send it back\n"
            + "!virustotal [url] - send url to virustotal \n"
            + "!urlhaus [url] - send url to urlhaus \n"
            + "!geoip [url] - send url to geoip \n"
            + "!history [url] - get url redirect path \n"
            + "\n_If you have any question ask:_\n"
            + "my creator: https://t.me/trulr"
        )
        return help_message

    async def _index_command(self, channel):
        try:
            response = requests.get(f"{self.urlanalyser_url}")
            if response.status_code == 200:
                answer = response.json()["message"]
        except Exception as error:
            answer = "Something went wrong"
            self.logger.error(f"Error happened: {error}")
        return answer


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
        if req.startswith("!help"):
            return self._set_helper_text()
        if req.startswith("!index"):
            return await self._index_command(channel)

        if urls == []:
            return "Missing URL"
        else:
            return await self._choose_command(urls, req, channel)

    async def _choose_command(self, urls:list, message: str, channel) -> str:
        settings = {
                "urlhaus": False,
                "virustotal": False,
                "geoip": False,
                "history": False,
            }
        screenshot = False
        ask_api = True
        answer = ""
        if message.startswith("!url"):
            settings["urlhaus"] = True
            settings["virustotal"] = True
            settings["geoip"] = True
            settings["history"] = True
            screenshot = True
        elif message.startswith("!urlhaus"):
            settings["urlhaus"] = True
        elif message.startswith("!virustotal"):
            settings["virustotal"] = True
        elif message.startswith("!geoip"):
            settings["geoip"] = True
        elif message.startswith("!history"):
            settings["history"] = True
        elif message.startswith("!screenshot"):
            screenshot = True
            ask_api = False
        else:
            settings["urlhaus"] = True
            settings["virustotal"] = True
            settings["geoip"] = True
            settings["history"] = True
            screenshot = True
        for url in urls:
            settings["url"] = url
            if ask_api:
                answer = self._ask_urlanalyser_api(url, settings)
                for key in answer.keys():
                    result = str(answer[key])
                    await self._send_answer(f"**{key}**: {result}", channel)
            if screenshot:
                await self._send_screenshot(url, channel)
        return str(answer)

    def _ask_urlanalyser_api(self, url: str, settings: dict) -> dict:
        try:
            response = requests.post(f"{self.urlanalyser_url}/get_infos", json=settings)
            if response.status_code == 200:
                return response.json()["result"]
            else:
                return {
                    "error": f"Error happened with url: {url} - status code: {response.status_code}"
                }
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            return {"error": f"Error happened with url: {url}"}

    async def _send_screenshot(self, url: str, channel) -> str:
        await self._send_answer(
            f"Taking screenshot can be slow - thank for your patient",
            channel,
        )
        response = requests.get(
            f"{self.urlanalyser_url}/get_screenshot?url={self._encode_url(url)}"
        )
        if response.status_code == 200:
            name = "screenshot"
            image_file = discord.File(
                io.BytesIO(response.content), filename=f"{name}.png"
            )
            await channel.send(file=image_file)
        else:
            await self._send_answer(
                f"Error happened while creating screenshot url: {url} - status code: {response.status_code}",
                channel,
            )
        try:
            pass
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            await self._send_answer(f"Error happened with url: {url}", channel)

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()

    def _decode_url(self, url: str):
        return base64.urlsafe_b64decode(url.encode()).decode()
