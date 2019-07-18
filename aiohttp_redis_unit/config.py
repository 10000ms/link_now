import os


class ProductionConfig:
    pass


class DevelopmentConfig:

    SERVER_CONFIG = {
        'host': '0.0.0.0',
        'port': '8081',
    }

    SERVER_LOGGER_NAME = 'server.'

    REPORTER_LOGGER_NAME = 'reporter.'

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    REDIS_HOST = 'redis'

    REDIS_PORT = '6379'

    SESSION_DB = 0

    MESSAGE_DB = 1

    REMOTE_DB = 2

    GROUP_DB = 3

    REMOTE_NAME = 'remote'

    SESSION_EXPIRE = 180

    MONGODB_URL = {
        'host': 'aiohttp-mongdb-unit',
        'port': '9988',
    }


config = DevelopmentConfig
