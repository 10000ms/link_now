"""
    config
    ~~~~~~~~~

    配置信息模块

    :copyright: (c) 2018 by Victor Lai.

"""
import os


# 项目文件夹路径
BASE_DIR = os.path.dirname(__file__)


# server options
options = {
    'port': 9040,
}

# server settings
settings = {
    'debug': True,   # debug模式

    'static_path': os.path.join(BASE_DIR, 'static'),  # 静态文件地址
    'template_path': os.path.join(BASE_DIR, 'template'),  # 模板文件地址

    'cookie_secret': '7BEnV14KSXKwl0ag1f/MzM0g4xXuDknkkTkz4LRFUUo=',  # 安全cookie秘钥，跨站攻击防护必须
    'xsrf_cookies': True,  # 跨站脚本攻击防护
}


aiohttp_redis_unit = {
    'host': 'aiohttp-redis-unit',
    'port': 8081,
}

internal_host = 'webapp:9040'


aiohttp_mongodb_unit = {
    'host': 'aiohttp-mongdb-unit',
    'port': 9988,
}

trust_list = [
    '127.0.0.1',
    'localhost',
    'aiohttp-mongodb-unit',
    'aiohttp-redis-unit',
]
