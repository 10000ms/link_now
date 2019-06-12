# -*- coding: utf-8 -*-
import unittest

from server.handler import session
from config import config


def need_test_list():
    test_list = [
        'test_add_session_db',
        'test_check_session_db',
        'test_delete_session_db',
    ]
    return test_list


class ServerTest(unittest.TestCase):
    test_data_key = '111'
    test_data_value = 'asdas4d56as4d35'
    test_remote = '127.0.0.1'
    test_handler = session.SessionHandler()

    def test_add_session_db(self):
        self.test_handler.add_session_db(self.test_data_key, self.test_data_value)
        test_data = self.test_handler.session_db.get(self.test_data_key)
        assert test_data == self.test_data_value

    def test_check_session_db(self):
        self.test_handler.session_db.set(self.test_data_key, self.test_data_value)
        res = self.test_handler.check_session_db(self.test_remote, self.test_data_key, self.test_data_value)
        get_remote = self.test_handler.remote_db.get(self.test_data_key)
        has_remote = self.test_handler.remote_db.sismember(config.REMOTE_NAME, self.test_remote)
        assert res is True
        assert get_remote == self.test_remote
        assert has_remote is True

    def test_delete_session_db(self):
        self.test_handler.remote_db.set(self.test_data_key, self.test_data_value)
        self.test_handler.delete_session_db(self.test_data_key)
        res = self.test_handler.remote_db.exists(self.test_data_key)
        assert res is False
