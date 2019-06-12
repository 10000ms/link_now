# -*- coding: utf-8 -*-
import unittest

from test import (
    redis_test,
    server_session_test,
    server_message_test,
)


if __name__ == '__main__':
    test_case = unittest.TestSuite()
    test_case.addTest(redis_test.RedisTest('test_conn'))
    for test_func in server_session_test.need_test_list():
        test_case.addTest(server_session_test.ServerTest(test_func))
    test_case.addTest(server_message_test.ServerTest('test_add_message_db'))
    runner = unittest.TextTestRunner()
    runner.run(test_case)
