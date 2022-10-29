from logging import Logger, getLogger
from rethinkdb import RethinkDB


class DBConnector:
    logger: Logger
    rethink: RethinkDB

    def __init__(self, config: dict, logger: Logger):
        self.rethink = RethinkDB()
        self.rethink.connect("localhost", 28015).repl()

    def create_table(self, database: str, table: str) -> None:
        self.rethink.db(database).table_create(table).run()


if __name__ == "__main__":
    dbc = DBConnector({}, getLogger())
    dbc.create_table("test", "table")
