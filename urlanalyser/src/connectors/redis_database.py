from src.ancestor import Ancestor
from redis import Redis
from time import time


class RedisDatabase(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.redis = Redis(host="redis")

    def add_data(self, data: dict) -> bool:
        encoded_url = self._encode_url(data["url"])
        data["time"] = time()
        return self.redis.hset(encoded_url, mapping=data)

    def get_data(self, url: str) -> dict:
        encoded_url = self._encode_url(url)
        return self.redis.hgetall(encoded_url)

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()
