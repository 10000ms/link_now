import pymongo


class MongoConn:

    def __init__(self, host, port, db_name, username=None, password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password

        # connect db
        self.db = pymongo.MongoClient(
            '{}:{}'.format(self.host, self.port),
        )
        self.db = self.db[self.db_name]
        self.connected = True
