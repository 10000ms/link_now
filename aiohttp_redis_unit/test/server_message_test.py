# -*- coding: utf-8 -*-
import unittest
import json

from server.handler import message


class ServerTest(unittest.TestCase):
    test_data_key = '111'
    test_message_type = 2
    test_message_type_id = 11
    test_message = 'asdas4d56as4d35'
    test_handler = message.MessageHandler()

    def test_add_message_db(self):
        res = self.test_handler.add_message_db(
            self.test_data_key,
            self.test_message_type,
            self.test_message_type_id,
            self.test_message
        )
        assert res is True
        get_message = self.test_handler.message_db.lindex(str(self.test_message_type), 0)
        json_message = {
            'id': self.test_message_type_id,
            'message': self.test_message,
        }
        json_message = json.dumps(json_message)
        assert get_message == json_message

