# -*- coding: utf-8 -*-
import functools
import json

import aiohttp
from aiohttp import web

from config import config
from server.handler import error
from utils import set_logging
from redis_part import RedisConn


class ServerComponent:
    logger = set_logging(config.SERVER_LOGGER_NAME)
    session_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.SESSION_DB
    ).db
    message_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.MESSAGE_DB
    ).db
    remote_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REMOTE_DB
    ).db


async def get_json_date(request, need_len=None):
    data = await request.content.read()
    data = data.decode()
    data = json.loads(data)
    ServerComponent.logger.info(data)
    if need_len is None or len(data) == need_len:
        return data


def check_remote(func):
    @functools.wraps(func)
    def wrapper(request):
        if request.remote in config.TRUST_LIST:
            return func(request)
        else:
            return error.handle_403()
    return wrapper


def async_check_remote(func):
    @functools.wraps(func)
    async def wrapper(request):
        if request.remote in config.TRUST_LIST:
            return await func(request)
        else:
            return error.handle_403()
    return wrapper


def general_json_data(status, info_dict=None):
    status_data = {'status': status}
    if info_dict is not None:
        info_dict.update(status_data)
    else:
        info_dict = status_data
    return info_dict


def get_data(func):
    @functools.wraps(func)
    async def wrapper(request):
        get_json = await get_json_date(request)
        if get_json is not None:
            return func(get_json)
        else:
            return error.handle_400()
    return wrapper


def async_get_data(func):
    @functools.wraps(func)
    async def wrapper(request):
        get_json = await get_json_date(request)
        if get_json is not None:
            return await func(get_json)
        else:
            return error.handle_400()
    return wrapper


def ok_response():
    res_data = general_json_data('ok')
    return web.json_response(data=res_data)


async def fetch(session, url, data):
    ServerComponent.logger.info('发生post：' + str(url) + str(data))
    async with session.post(url, data=data) as response:
        return await response.text()


async def server_aio_client(url, data):
    async with aiohttp.ClientSession() as session:
        ServerComponent.logger.info('启动main_reporter')
        res = await fetch(session, url, data)
        return res


async def get_mongo_fetch_data(data, url):
    json_data = json.dumps(data)
    mongo_url = \
        'http://' \
        + config.MONGODB_URL['host'] \
        + ':' \
        + str(config.MONGODB_URL['port']) \
        + url
    res = await server_aio_client(mongo_url, json_data)
    return json.loads(res)
