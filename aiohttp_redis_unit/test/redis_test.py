# -*- coding: utf-8 -*-
import unittest

from redis_part import RedisConn
from config import config


class RedisTest(unittest.TestCase):
    test_data_key = 'Test'
    test_data_value = '111'

    def setUp(self):
        self.redis_conn = RedisConn(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.SESSION_DB
        )

    def test_conn(self):
        self.redis_conn.db.set(self.test_data_key, self.test_data_value)
        test_data = self.redis_conn.db.get(self.test_data_key)
        assert test_data == self.test_data_value
        self.redis_conn.db.delete(self.test_data_key)

    def tearDown(self):
        self.redis_conn.pool.disconnect()
