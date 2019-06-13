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
    'port': 4000,
}

# server settings
settings = {
    'debug': False,   # debug模式

    'static_path': os.path.join(BASE_DIR, 'static'),  # 静态文件地址
    'template_path': os.path.join(BASE_DIR, 'template'),  # 模板文件地址

    'cookie_secret': '7BEnV14KSXKwl0ag1f/MzM0g4xXuDknkkTkz4LRFUUo=',  # 安全cookie秘钥，跨站攻击防护必须
    'xsrf_cookies': True,  # 跨站脚本攻击防护
    'local_url': '47.106.211.149'
}


aiohttp_redis_unit = {
    'host': 'localhost',
    'port': 8081,
}


aiohttp_mongodb_unit = {
    'host': 'localhost',
    'port': 9988,
}

trust_list = [
    '127.0.0.1',
    'localhost',
    '47.106.211.149',
]
