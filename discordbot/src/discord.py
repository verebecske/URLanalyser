from discord.ext import tasks, commands
import discord
from src.ancestor import Ancestor
from logging import DEBUG
import re
import requests
import base64
import io


class MaliciousContentError(Exception):
    def __str__(self):
        return "Woop-woop someone send something wrong!"


class ServerError(Exception):
    pass


class DBot(Ancestor):
    mytoken: str
    intents: discord.Intents

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
        if config["debug"] == "true":
            self.logger.setLevel(DEBUG)

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
        bot.set_urlanalyser(self.config)
        bot.run(self.config["token"])


class DiscordClient(commands.Bot, Ancestor):
    debug = False

    def __init__(self, command_prefix, intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        Ancestor.__init__(self)
        self.logger.info("Start DiscordClient")

    def set_urlanalyser(self, config: dict) -> None:
        self.config = config
        self.urlanalyser_url = (
            f"http://{config['urlanalyser_host']}:{config['urlanalyser_port']}"
        )

    def _set_log_channel(self) -> None:
        try:
            for channel in self.get_all_channels():
                if (
                    channel.guild == self.config["server"]
                    and channel.name == self.config["log_channel"]
                ):
                    break
            self.log_channel = channel
        except Exception as error:
            self.logger.error(f"Error happened while setting log channel: {error}")
            self.log_channel = None

    # Discord default

    async def send_message(self, channel: discord.channel, text):
        self.logger.info(f"I send: {str(text)}\nin channel: {str(channel)}")
        try:
            await channel.send(text)
        except Exception as error:
            self.logger.error(f"Error occurred during message sending error={error}")

    async def on_message_delete(self, message):
        msg = f"The message of {message.author} was deleted: {message.content}"
        try:
            if self.log_channel is not None:
                await self.log_channel.send(msg)
        except Exception as error:
            self.logger.warning(f"Maybe is log channel didn't set error={error}")

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
        try:
            if message.author == self.user:
                return
            self.logger.info(
                f"I got: {message.content}\nin channel: {str(message.channel)}\nfrom: {str(message.author)}"
            )
            if self.debug:
                replay = f"**{message.author}** sent me:\n\t{message.content}"
                await self._send_answer(replay, message.channel)
            if message.channel.type == discord.ChannelType.private:
                return await self._read_direct_message(
                    message.content, message.author, message.channel
                )
            else:
                try:
                    return await self._read_message_on_server(
                        message.content, message.author, message.channel
                    )
                except MaliciousContentError as error:
                    await self._delete_message(message)
                    await self._send_answer("Message was deleted because it contains a malicious URL", message.channel)
                    return
        except Exception as error:
            self.logger.error(f"Client error: {error}")
            await self._send_answer("Client error happened", message.channel)

    async def _read_message_on_server(self, content, author, channel) -> str:
        url_list = self._filter_urls(content)
        if await self._is_malicious_list(url_list):
            raise MaliciousContentError("Find malicious content")

    async def _is_malicious_list(self, url_list: list) -> bool:
        is_malicious = False
        for url in url_list:
            is_malicious = is_malicious or await self._check_url(url)
        self.logger.info(f"Results: {is_malicious}")
        return is_malicious

    async def _delete_message(self, message):
        await message.delete()

    async def _send_answer(self, message, channel):
        while len(message) > 2000:
            await channel.send(message[:2000])
            message = message[2000:]
        await channel.send(message)

    def _filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        urls = [t[0] for t in re.findall(pattern, message)]
        self.logger.info(f"URLS: {urls}")
        return urls


    async def _check_url(self, url: str) -> bool:
        try:
            result = await self.send_get_request("check", url)
            return result.json()["result"]["is_malicious"]
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
        return False

    async def _help_handler(self, channel) -> str:
        message = (
            "**Commands:**\n"
            + "!help - send this text\n"
            + "!index - perform health-check\n"
            + "!check <url> - just a quick test about the url, the result is yes or no\n"
            + "!screenshot <url> - create a screenshot about the webpage and send it back\n"
            + "!virustotal <url> - send url to virustotal \n"
            + "!urlhaus <url> - send url to urlhaus \n"
            + "!location <url> - the location of the domain IP address with geoip search\n"
            + "!redirection <url> [-v] - get url redirections pass -v for verbose mode\n"
            + "!domain_age <url> - return the domain age\n"
            + "!domain_reputation <url> - calculate the domain reputation from IP block lists\n"
            + "!download <url> - download the page source as zip\n"
            + "\n_If you have any question ask:_\n"
            + "my creator:\n\t https://t.me/trulr"
        )
        return await self._send_answer(message, channel)

    async def send_get_request(self, endpoint, url, extras: dict = None):
        if extras is None:
            _extras = ""
        else:
            _extras = "".join([f"&{key}={value}" for key, value in extras.items()])
        try:
            url = self._encode_url(url)
            response = requests.get(
                f"{self.urlanalyser_url}/{endpoint}?url={url}{_extras}"
            )
            self.logger.debug(f"Server response: {response}")
            if response.status_code == 200:
                return response
            else:
                self.logger.error(f"Server error happened: {response.text}")
                raise ServerError(response.text)
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            raise

    async def _read_direct_message(self, content, author, channel) -> str:
        try:
            urls = self._filter_urls(content)
            if content.startswith("!help"):
                return await self._help_handler(channel)
            if content.startswith("!index"):
                return await self._index_handler(channel)
            if urls == []:
                if content.startswith("!"):
                    return await self._send_answer("Missing URL", channel)
                else:
                    return await self.send_message(channel, content)
            else:
                return await self._choose_handler(urls, content, channel)
        except ServerError as error:
            self.logger.error(f"Error happened: {error}")
            return await self._send_answer(f"Server error happened: {error}", channel)

    async def _choose_handler(self, urls: list, content: str, channel) -> str:
        if content.startswith("!domain_age"):
            return await self._domain_age_handler(urls, channel)
        if content.startswith("!domain_reputation"):
            return await self._domain_reputation_handler(urls, channel)
        if content.startswith("!download"):
            return await self._download_handler(urls, channel)
        if content.startswith("!redirection"):
            return await self._redirection_handler(urls, content, channel)
        if content.startswith("!location"):
            return await self._location_handler(urls, channel)
        if content.startswith("!check"):
            return await self._check_url_handler(urls, channel)
        if content.startswith("!screenshot"):
            return await self._screenshot_handler(urls, channel)
        if content.startswith("!virustotal"):
            return await self._virustotal_handler(urls, channel)
        if content.startswith("!urlhaus"):
            return await self._urlhaus_handler(urls, channel)
        if content.startswith("!"):
            return await self._unknown_handler(content, channel)
        return await self._check_url_handler(urls, channel)

    # Handlers

    async def _virustotal_handler(self, urls, channel):
        settings = {
            "urlhaus": False,
            "virustotal": True,
            "geoip": False,
            "redirection": False,
        }
        for url in urls:
            response = await self._get_info_handler(url, settings)
            answer = self._format_answer(response)
            await self._send_answer(answer, channel)

    async def _urlhaus_handler(self, urls, channel):
        settings = {
            "urlhaus": True,
            "virustotal": False,
            "geoip": False,
            "redirection": False,
        }
        for url in urls:
            response = await self._get_info_handler(url, settings)
            answer = self._format_answer(response)
            await self._send_answer(answer, channel)

    async def _get_info_handler(self, url: str, settings: dict) -> dict:
        try:
            settings["url"] = url
            response = requests.post(f"{self.urlanalyser_url}/get_info", json=settings)
            if response.status_code == 200:
                return response.json()["result"]
            else:
                return {
                    "error": f"Error happened with url: {url} - status code: {response.status_code}"
                }
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            return {"error": f"Error happened with url: {url}"}

    async def _index_handler(self, channel):
        try:
            response = requests.get(f"{self.urlanalyser_url}")
            if response.status_code == 200:
                answer = response.json()["result"]
        except Exception as error:
            answer = "Something went wrong"
            self.logger.error(f"Error happened: {error}")
        await self._send_answer(answer, channel)

    async def _unknown_handler(self, content, channel):
        cmd = content.split(" ")[0]
        answer = f"Unknown command: {cmd}"
        await self._send_answer(answer, channel)

    async def _screenshot_handler(self, urls, channel):
        for url in urls:
            await self._send_screenshot(url, channel)

    async def _check_url_handler(self, urls, channel):
        for url in urls:
            response = await self.send_get_request("check", url)
            answer = self._format_answer(response.json()["result"])
            await self._send_answer(answer, channel)

    async def _domain_age_handler(self, urls, channel):
        for url in urls:
            response = await self.send_get_request("get_domain_age", url)
            answer = self._format_answer(response.json()["result"])
            await self._send_answer(answer, channel)

    async def _domain_reputation_handler(self, urls, channel):
        for url in urls:
            response = await self.send_get_request("get_domain_reputation", url)
            answer = self._format_answer(response.json()["result"])
            await self._send_answer(answer, channel)

    async def _redirection_handler(self, urls, content, channel):
        if " -v " in content:
            extras = {"all": "True"}
        else:
            extras = None
        for url in urls:
            response = await self.send_get_request("get_redirection", url, extras)
            answer = self._format_answer(response.json()["result"])
            await self._send_answer(answer, channel)

    async def _location_handler(self, urls, channel):
        for url in urls:
            response = await self.send_get_request("get_location", url)
            answer = self._format_answer(response.json()["result"])
            await self._send_answer(answer, channel)

    async def _download_handler(self, urls, channel):
        await self._send_answer(
            f"Download a webpage can be slow - thank for your patience",
            channel,
        )
        for url in urls:
            response = requests.get(
                f"{self.urlanalyser_url}/download_as_zip?url={self._encode_url(url)}"
            )
        if response.status_code == 200:
            name = "page"
            image_file = discord.File(
                io.BytesIO(response.content), filename=f"{name}.zip"
            )
            await channel.send(file=image_file)
        else:
            await self._send_answer(
                f"Error happened while sending zip file: {url} - status code: {response.status_code}",
                channel,
            )
        try:
            pass
        except Exception as error:
            self.logger.error(f"Error happened: {error}")
            await self._send_answer(f"Error happened with url: {url}", channel)

    async def _send_screenshot(self, url: str, channel) -> str:
        await self._send_answer(
            f"Taking screenshot can be slow - thank for your patience",
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

    def _format_dict(self, result) -> str:
        text = ""
        for key, value in result.items():
            text += f"**{key}**: {value}\n"
        return text

    def change_https(self, match_obj):
        if match_obj.group() is not None:
            return f"<->{match_obj.group()}<->"

    def _disable_link_preview(self, text: str) -> str:
        url_regex = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
        return re.sub(url_regex, self.change_https, text)

    def _format_answer(self, result) -> str:
        if isinstance(result, dict):
            text = self._format_dict(result)
        elif isinstance(result, list):
            text = ""
            for value in result:
                if isinstance(value, dict):
                    text += self._format_dict(value) + "\n"
                else:
                    text += f"{value}\n"
        else:
            text = result
        return self._disable_link_preview(text)
