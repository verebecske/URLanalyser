from src.ancestor import Ancestor
from redis import Redis
from time import time


class BlockListDatabaseFactory(Ancestor):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def get_blocklistdb(self):
        if self.config["redis"]:
            return RedisDatabase(self.config)
        return DefaultDatabase()


class BlockListDatabase(Ancestor):
    def add_to_database(self, type, data, source):
        pass

    def get_from_database(self, type, data) -> list:
        pass


class DefaultDatabase(BlockListDatabase):
    def __init__(self):
        super().__init__()
        self.in_memory_bad_ips = defaultdict(list)
        self.in_memory_bad_urls = defaultdict(list)

    def add_to_database(self, type, data, source):
        if self.database is None:
            match type:
                case "ip":
                    return self.in_memory_bad_ips[ip].append(filename)
                case "url":
                    return self.in_memory_bad_urls[line].append(filename)

    def get_from_database(self, type, data) -> list:
        if self.database is None:
            match type:
                case "ip":
                    return self.in_memory_bad_ips.get(ip_addr, [])
                case "url":
                    return self.in_memory_bad_urls.get(url, [])


class RedisDatabase(BlockListDatabase):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.redis = Redis(host="redis")

    def add_to_database(self, data_type, data, source):
        self.logger.error(f"add redis {data_type}-{data}")
        res = self.redis.lpush(f"{data_type}-{data}", source)
        self.logger.error(f"add redis {res}")

    def get_from_database(self, data_type, data) -> list:
        self.logger.error(f"get redis {data_type}-{data}")
        res = self.redis.lrange(f"{data_type}-{data}", 0, -1)
        self.logger.error(f"get redis {res}")
        return list(map(str, res))

    def add_data(self, data: dict) -> bool:
        encoded_url = self._encode_url(data["url"])
        data["time"] = time()
        return self.redis.hset(encoded_url, mapping=data)

    def get_data(self, url: str) -> dict:
        encoded_url = self._encode_url(url)
        return self.redis.hgetall(encoded_url)

    def _encode_url(self, url: str):
        return base64.urlsafe_b64encode(url.encode()).decode()


class OldRedisDatabase(Ancestor):
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
