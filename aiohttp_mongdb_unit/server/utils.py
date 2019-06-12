# -*- coding: utf-8 -*-
import functools
import json

from aiohttp import web

from config import config
from server.handler import error
from utils import set_logging
from mongo_part import MongoConn


class ServerComponent:
    logger = set_logging(config.SERVER_LOGGER_NAME)
    db = MongoConn(
        config.MONGODB['host'],
        config.MONGODB['port'],
        config.MONGODB['db_name'],
        config.MONGODB['username'],
        config.MONGODB['password'],
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
        print(request)
        if request.remote in config.TRUST_LIST:
            return func(request)
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


def no_list():
    emtpy_list = []
    return json.dumps(emtpy_list)


def ok_response():
    res_data = general_json_data('ok')
    return web.json_response(data=res_data)
