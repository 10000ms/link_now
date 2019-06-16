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
            # connect db
            self.db = pymongo.MongoClient(
                'mongodb://{}:{}/'.format(self.host, self.port),
                username=self.username,
                password=self.password,
                authSource=self.db_name)
            self.connected = True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)
