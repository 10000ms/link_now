# -*- coding: utf-8 -*-
"""
    redis_app
    ~~~~~~~~~

    redis连接类模块

    :copyright: (c) 2018 by Victor Lai.

"""
import redis


class RedisConn(object):

    def __init__(self, host, port, password=None, decode_responses=True):
        self.host = host
        self.port = port
        self.password = password
        self.decode_responses = decode_responses

        if password:
            self.pool = redis.ConnectionPool(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=self.decode_responses
            )
        else:
            self.pool = redis.ConnectionPool(
                host=self.host,
                port=self.port,
                decode_responses=self.decode_responses
            )
        self.db = redis.Redis(connection_pool=self.pool)
