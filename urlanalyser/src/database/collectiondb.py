from src.ancestor import Ancestor
from redis import Redis

class CollectionDatabase(Ancestor):
    def add_to_database(self, name, data, metadata):
        pass

    def get_from_database(self, name):
        pass

class DefaultCollectionDatabase(CollectionDatabase):
    def __init__(self):
        super().__init__()
        self.default_path = ""

    def add_to_database(self, name, data, metadata):
        # create folder with name
        # save file to folder with name
        # write metadata to txt file :D
        pass

    def get_from_database(self, name):
        pass


class RedisCollectionDatabase(CollectionDatabase):

    def __init__(self, config: dict):
        super().__init__()
        self.redis = Redis(host=config["redis_host"])

    def add_to_database(self, name, data, metadata):
        pass

    def get_from_database(self, name):
        pass