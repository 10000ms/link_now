"""
    utils
    ~~~~~~~~~

    协助方法


    :copyright: (c) 2018 by Victor Lai.

"""
import json
import logging
import time
import sys
from enum import Enum

from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPRequest,
)

import config
from Log import get_logfile


async def get_mongo_fetch_data(data, url):
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
    res = await get_fetch_data(data, mongo_url)
    str_res = res.body
    return str_res.decode()


async def get_redis_fetch_data(data, url):
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
    res = await get_fetch_data(data, redis_url)
    str_res = res.body
    return str_res.decode()


async def get_fetch_data(data, url):
    json_data = json.dumps(data)
    http_client = AsyncHTTPClient()
    request = HTTPRequest(
        url=url,
        method='POST',
        body=json_data,
    )
    return await http_client.fetch(request)


def set_logging(part):
    this_logger = logging.getLogger(part)
    this_logger.setLevel(logging.INFO)
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = part + rq + '.log'
    logfile = get_logfile(log_name)
    fh = logging.FileHandler(logfile, mode='w', encoding='UTF-8')
    fh.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    this_logger.addHandler(fh)
    this_logger.addHandler(sh)
    this_logger.info('启动' + part + '记录器')
    return this_logger


class MessageType(Enum):
    user_message = 1
    group_message = 2
    all_message = 3
    system_message = 4
