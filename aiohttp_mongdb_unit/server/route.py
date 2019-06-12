# -*- coding: utf-8 -*-
from aiohttp import web

from server.handler import user


def route():
    route_list = [
        web.post('/user/login', user.login),
        web.post('/user/register', user.register),
        web.post('/user/get_user_info', user.get_user_info),
        web.post('/user/get_user_friend', user.get_user_friend),
        web.post('/user/user_add_friend', user.user_add_friend),
        web.post('/user/user_join_group', user.user_join_group),
        web.post('/user/get_group', user.get_group),
        # web.post('/user/change_group', user.change_group),
        web.post('/user/create_group', user.create_group),
        # web.post('/user/get_all_group', user.get_all_group),
    ]
    return route_list
