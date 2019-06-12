# -*- coding: utf-8 -*-
from aiohttp import web


def handle_400():
    info_dict = {'info': '请求有误'}
    data = error_json_data(400, info_dict)
    return web.json_response(data=data, status=400)


def handle_403():
    info_dict = {'info': '不被允许的请求'}
    data = error_json_data(403, info_dict)
    return web.json_response(data=data, status=403)


def handle_500():
    info_dict = {'info': '服务器内部错误'}
    data = error_json_data(500, info_dict)
    return web.json_response(data=data, status=500)


def error_json_data(status, info_dict=None):
    status_data = {'status': status}
    if info_dict is not None:
        info_dict.update(status_data)
    else:
        info_dict = status_data
    return info_dict
