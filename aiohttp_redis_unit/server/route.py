# -*- coding: utf-8 -*-
from aiohttp import web

from server.handler import session
from server.handler import message


def route():
    route_list = [
        web.post('/session/add', session.add_session),
        web.post('/session/check_session', session.check_session),
        web.post('/session/check_login', session.check_login),
        # web.post('/session/delete', session.delete_session),
        web.post('/message/add', message.add_message),
        web.post('/message/user_login', message.user_login),
        web.post('/message/user_logout', message.user_logout),
        web.post('/message/add_friend', message.add_friend),
        web.post('/message/add_group', message.add_group),
        web.post('/message/create_group', message.create_group),
    ]
    return route_list
