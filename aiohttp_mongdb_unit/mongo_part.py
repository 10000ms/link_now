# -*- coding: utf-8 -*-
import pymongo


class MongoConn:

    def __init__(self, host, port, db_name, username=None, password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password

        # connect db
        self.conn = pymongo.MongoClient(self.host, self.port)
        self.db = self.conn[self.db_name]  # connect db
        if self.username and self.password:
            self.connected = self.db.authenticate(self.username, self.password)
        else:
            self.connected = True
