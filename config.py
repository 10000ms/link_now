# -*- coding: utf-8 -*-
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
    "port": 8011,
}

# server settings
settings = {
    "debug": True,   # debug模式

    "static_path": os.path.join(BASE_DIR, "static"),  # 静态文件地址
    "template_path": os.path.join(BASE_DIR, "template"),  # 模板文件地址

    "cookie_secret": "7BEnV14KSXKwl0ag1f/MzM0g4xXuDknkkTkz4LRFUUo=",  # 安全cookie秘钥，跨站攻击防护必须
    "xsrf_cookies": True,  # 跨站攻击防护
    "local_url": "127.0.0.1"
}


# mongodb settings
mongodb = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'link_now',
    'username': None,
    'password': None
}


# redis settings
redis = {
    'host': 'localhost',
    'port': 6379,
    'password': None
}


aiohttp_redis_unit = {
    'host': 'localhost',
    'port': 6379,
}


aiohttp_mongodb_unit = {
    'host': 'localhost',
    'port': 9988,
}
