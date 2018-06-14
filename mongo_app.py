# -*- coding: utf-8 -*-
"""
    mongo_app
    ~~~~~~~~~

    mongo连接类模块

    :copyright: (c) 2018 by Victor Lai.

"""
import pymongo
import sys
import traceback


class MongoConn(object):

    def __init__(self, host, port, db_name, username=None, password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password

        # connect db
        try:
            self.conn = pymongo.MongoClient(self.host, self.port)
            self.db = self.conn[self.db_name]  # connect db
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)
