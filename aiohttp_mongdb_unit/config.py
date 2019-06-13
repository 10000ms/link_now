# -*- coding: utf-8 -*-
class ProductionConfig:
    pass


class DevelopmentConfig:

    SERVER_CONFIG = {
        'host': '0.0.0.0',
        'port': '9988',
    }

    SERVER_LOGGER_NAME = 'server.'

    MONGODB = {
        'host': 'mongo',
        'port': 27017,
        'db_name': 'user',
        'username': 'root',
        'password': '123456',
    }


config = DevelopmentConfig
