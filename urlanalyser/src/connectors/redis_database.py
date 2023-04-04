from src.ancestor import Ancestor
from redis import Redis

class RedisDatabase(Ancestor):
    config: dict

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.redis = Redis(host="redis")

    def add_data(self, data):
        pass

    def get_data(self, id):
        pass

    def check_data(self, data):
        visits = self.redis.incr('counter')
        return visits
