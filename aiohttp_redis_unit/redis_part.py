# -*- coding: utf-8 -*-
import redis


connection_pool_dict = {}


class RedisConn:

    def __init__(self, host, port, password=None, db=0, decode_responses=True):
        connection_pool_key = str(host) + ':' + str(port) + ':' + str(db)
        if not connection_pool_dict.get(connection_pool_key):
            if password is None:
                new_pool = redis.ConnectionPool(
                    host=host,
                    port=port,
                    db=db,
                    decode_responses=decode_responses
                )
            else:
                new_pool = redis.ConnectionPool(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=decode_responses
                )
            connection_pool_dict[connection_pool_key] = new_pool
        self.pool = connection_pool_dict[connection_pool_key]
        self.db = redis.Redis(connection_pool=self.pool)
