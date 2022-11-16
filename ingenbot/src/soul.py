import re

class Soul:
    debug = False

    async def send_answer(self, message, channel):
        pass

    async def read_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")

        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self.send_answer(replay, channel)

        url_list = self.filter_urls(req)
        if self.is_malicious_list(url_list):
            replay = "But Tom, that's what I do, and I plan on eating you slowly!"
        else:
            replay = "We're not unreasonable, I mean, no one's gonna eat your eyes"
        return replay

    def filter_urls(self, message: str) -> list:
        pattern = r"((http(s)?://)?([a-z0-9-]+\.)+[a-z0-9]+(/.*)?)"
        x = [t[0] for t in re.findall(pattern, message)]
        print("URLS:", x)
        return x

    def is_malicious_list(self, url_list: list) -> bool:
        is_malicious = False
        for url in url_list:
            is_malicious = is_malicious or self.inspect_url(url)
        print("Results:", is_malicious)
        return is_malicious

    def inspect_url(self, url: str) -> bool:
        mock_list = [
            "napszemuveg.be",
            "reallykaros.io",
        ]
        return url in mock_list

    async def read_direct_message(self, message) -> str:
        req: str = message["content"]
        user: str = message["author"]
        channel = message["channel"]
        print(f"I got: {message}\nin channel: {str(channel)}\nfrom: {str(user)}")

        if self.debug:
            replay = f"Ezt küldted **{user}**:\n\t{req}"
            await self.send_answer(replay, channel)

        urls = self.filter_urls(req)
        if urls == []:
            replay = "Hey Tom, it's Bob!"
        else:
            replay = await self.send_to_analyser(urls)
        return replay

    async def send_to_analyser(self, urls: list):
        mock_ans = "I'd like to help you, Tom, in any way I can\n"
        mock_ans += "I sure appreciate the way you're working with me\n"
        mock_ans += "I'm not a monster, Tom, well, technically I am"
        return mock_ans
