# -*- coding: utf-8 -*-
import json

from server.utils import (
    async_check_remote,
    check_remote,
    ServerComponent,
    async_get_data,
    get_data,
    ok_response,
    get_mongo_fetch_data,
)
from utils import MessageType
from server.handler import error
from server.handler import session


class MessageHandler:
    Log = ServerComponent.logger
    message_db = ServerComponent.message_db
    remote_db = ServerComponent.remote_db

    @classmethod
    def add_message_db(cls, get_message_type, target_id, sender_id, sender_name, message):
        message_type = MessageType(int(get_message_type)).name
        is_login = True
        if message_type == MessageType.user_message and not cls.check_is_still_login(target_id):
            is_login = False
        if is_login:
            json_message = {
                'type': get_message_type,
                'id': target_id,
                'account': sender_id,
                'name': sender_name,
                'message': message,
            }

            # old version:
            # json_message = {
            #                 'sender': account,
            #                 'id': type_id,
            #                 'message': message,
            #                 'message_type': get_message_type,
            #             }

            json_message = json.dumps(json_message)
            cls.message_db.lpush(str(get_message_type), json_message)
            cls.Log.info(
                '添加message:' + json_message
            )
        return True

    @classmethod
    def check_is_still_login(cls, account):
        return cls.remote_db.exists(account)

    @classmethod
    def system_message(cls, target_account, message):
        return cls.add_message_db(
            MessageType.system_message.value,
            target_account,
            '1',
            '系统消息',
            message
        )

    @classmethod
    def system_all_message(cls, message):
        return cls.add_message_db(
            MessageType.all_message.value,
            '1',
            '1',
            '系统消息',
            message
        )

    @classmethod
    def system_group_message(cls, group_id, message):
        return cls.add_message_db(
            MessageType.group_message.value,
            group_id,
            '1',
            '系统消息',
            message
        )

    @classmethod
    def now_login_users(cls):
        return cls.remote_db.keys()


@check_remote
@get_data
def add_message(data):
    try:
        MessageHandler.add_message_db(
            data['type'],
            data['id'],
            data['account'],
            data['name'],
            data['message']
        )
    except BaseException as e:
        MessageHandler.Log.exception(e)
        return error.handle_500()
    return ok_response()


@async_check_remote
@async_get_data
async def user_login(data):
    send_data = {
        'account': data['account']
    }
    login_user_friends = await get_mongo_fetch_data(send_data, '/user/get_user_friend')
    now_login_users = MessageHandler.now_login_users()
    user_login_friends = []
    all_message = '用户: ' + str(data['username']) + ' 上线'
    MessageHandler.system_all_message(all_message)
    for user in now_login_users:
        if user in login_user_friends['friend']:
            user_login_friends.append(user)
            friend_message = {
                'method': 'add_login_friend',
                'm_id': [data['account'], ],
            }
            MessageHandler.system_message(user, friend_message)
    user_message = {
        'method': 'add_login_friend',
        'm_id': user_login_friends,
    }
    MessageHandler.system_message(data['account'], user_message)
    return ok_response()


@async_check_remote
@async_get_data
async def user_logout(data):
    send_data = {
        'account': data['account']
    }
    login_user_friends = await get_mongo_fetch_data(send_data, '/user/get_user_friend')
    now_login_users = MessageHandler.now_login_users()
    all_message = '用户: ' + str(data['username']) + ' 下线'
    MessageHandler.system_all_message(all_message)
    for user in now_login_users:
        if user in login_user_friends['friend']:
            friend_message = {
                'method': 'remove_login_friend',
                'm_id': data['account'],
            }
            MessageHandler.system_message(user, friend_message)
    try:
        session.SessionHandler.delete_session_db(data['account'])
    except BaseException as e:
        MessageHandler.Log.error(e)
        return error.handle_500()
    return ok_response()


@async_check_remote
@async_get_data
async def add_friend(data):
    res = await get_mongo_fetch_data(data, '/user/user_add_friend')
    if res['status'] == 'ok':
        now_login_users = MessageHandler.now_login_users()
        if data['account'] in now_login_users:
            owner_message = {
                'method': 'add_friend',
                'm_id': data['id'],
                'name': res['name']
            }
            MessageHandler.system_message(data['account'], owner_message)
        if data['id'] in now_login_users:
            friend_message = {
                'method': 'add_friend',
                'm_id': data['account'],
                'name': data['name']
            }
            MessageHandler.system_message(data['id'], friend_message)
        if data['account'] in now_login_users and data['id'] in now_login_users:
            owner_login_friend_message = {
                'method': 'add_login_friend',
                'm_id': [data['id'], ],
            }
            MessageHandler.system_message(data['account'], owner_login_friend_message)
            friend_login_friend_message = {
                'method': 'add_login_friend',
                'm_id': [data['account'], ]
            }
            MessageHandler.system_message(data['id'], friend_login_friend_message)
        return ok_response()
    else:
        return error.handle_500()


@async_check_remote
@async_get_data
async def add_group(data):
    res = await get_mongo_fetch_data(data, '/user/user_join_group')
    if res['status'] == 'ok':
        message = {
            'method': 'add_group',
            'm_id': data['id'],
            'name': res['name']
        }
        MessageHandler.system_message(data['account'], message)
        MessageHandler.system_group_message(data['id'], '用户: ' + data['name'] + ' 加入群聊')
        return ok_response()
    else:
        return error.handle_500()


@async_check_remote
@async_get_data
async def create_group(data):
    res = await get_mongo_fetch_data(data, '/user/create_group')
    if res['status'] == 'ok':
        message = {
            'method': 'create_group',
            'm_id': res['id'],
            'name': data['name']
        }
        MessageHandler.system_message(data['account'], message)
        return ok_response()
    else:
        return error.handle_500()
