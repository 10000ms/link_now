# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~~~~~

    协助方法


    :copyright: (c) 2018 by Victor Lai.

"""
import json

from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPRequest,
)

import config


def get_mongo_fetch_data(data, url):
    """
    包装异步mongo的fetch
    :param data: 原始可json的数据
    :param url: 路由
    :return: future对象，可以使用awiat来获得request对象
    """
    mongo_url = \
        'http://' \
        + config.aiohttp_mongodb_unit['host'] \
        + ':' \
        + str(config.aiohttp_mongodb_unit['port']) \
        + url
    return get_fetch_data(data, mongo_url)


def get_redis_fetch_data(data, url):
    """
    包装异步redis的fetch
    :param data: 原始可json的数据
    :param url: 路由
    :return: future对象，可以使用awiat来获得request对象
    """
    redis_url = \
        'http://' \
        + config.aiohttp_redis_unit['host'] \
        + ':' \
        + str(config.aiohttp_redis_unit['port']) \
        + url
    return get_fetch_data(data, redis_url)


def get_fetch_data(data, url):
    json_data = json.dumps(data)
    http_client = AsyncHTTPClient()
    request = HTTPRequest(
        url=url,
        method='POST',
        body=json_data,
    )
    return http_client.fetch(request)
