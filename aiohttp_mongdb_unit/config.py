# -*- coding: utf-8 -*-
class ProductionConfig:
    pass


class DevelopmentConfig:

    SERVER_CONFIG = {
        'host': '127.0.0.1',
        'port': '9988',
    }

    TRUST_LIST = [
        '127.0.0.1',
        'localhost',
        '47.106.211.149',
    ]

    SERVER_LOGGER_NAME = 'server.'

    MONGODB = {
        'host': 'localhost',
        'port': 27017,
        'db_name': 'user',
        'username': None,
        'password': None
    }


config = DevelopmentConfig
