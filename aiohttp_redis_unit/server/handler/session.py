# -*- coding: utf-8 -*-
import json

from aiohttp import web

from config import config
from server.utils import (
    check_remote,
    ServerComponent,
    get_data,
    general_json_data,
    ok_response,
)
from server.handler import error


class SessionHandler:
    Log = ServerComponent.logger
    session_db = ServerComponent.session_db
    remote_db = ServerComponent.remote_db

    @classmethod
    def add_session_db(cls, account, session):
        cls.session_db.setex(account, session, config.SESSION_EXPIRE)
        cls.Log.info('添加session:' + str(account) + ' ' + str(session))
        return True

    @classmethod
    def check_session_db(cls, remote, account, session):
        db_session = cls.session_db.get(account)
        if session == db_session:
            cls.change_session(remote, account)
            return True
        else:
            return False

    @classmethod
    def change_session(cls, remote, account):
        cls.session_db.delete(account)
        cls.remote_db.set(account, remote)
        if cls.remote_db.sismember(config.REMOTE_NAME, remote) is False:
            cls.remote_db.sadd(config.REMOTE_NAME, remote)

    @classmethod
    def delete_session_db(cls, account):
        cls.remote_db.delete(account)

    @classmethod
    def check_login(cls, account):
        session_db = cls.session_db.exists(account)
        remote_db = cls.remote_db.exists(account)
        return session_db is False and remote_db is False


@check_remote
@get_data
def add_session(data):
    try:
        SessionHandler.add_session_db(data['account'], data['session'])
    except BaseException as e:
        SessionHandler.Log.exception(e)
        return error.handle_500()
    return ok_response()


@check_remote
@get_data
def check_login(data):
    try:
        check = SessionHandler.check_login(data['account'])
    except BaseException as e:
        SessionHandler.Log.exception(e)
        return error.handle_500()
    if check:
        status = 'ok'
    else:
        status = 'error'
    data = general_json_data(status)
    return web.json_response(data=data)


@check_remote
@get_data
def check_session(data):
    try:
        check = SessionHandler.check_session_db(data['remote'], data['account'], data['session'])
    except BaseException as e:
        SessionHandler.Log.error(e)
        return error.handle_500()
    if check:
        status = 'ok'
    else:
        status = 'error'
    data = general_json_data(status)
    return web.json_response(data=data)


# @check_remote
# @get_data
# def delete_session(data):
#     try:
#         SessionHandler.delete_session_db(data['account'])
#     except BaseException as e:
#         SessionHandler.Log.error(e)
#         return error.handle_500()
#     return ok_response()
