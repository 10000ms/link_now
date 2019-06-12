# -*- coding: utf-8 -*-
import json
import uuid

from aiohttp import web

from server.utils import (
    check_remote,
    ServerComponent,
    get_data,
    general_json_data,
    no_list,
    ok_response,
)
from server.handler import error


class UserHandler:
    Log = ServerComponent.logger
    user_db = ServerComponent.db.user
    user_friend_db = ServerComponent.db.user_friend
    user_group_db = ServerComponent.db.user_group
    group_db = ServerComponent.db.group

    @classmethod
    def login(cls, account):
        get_user = cls.user_db.find_one({'account': account})
        res = {
            'password': get_user['password'],
            'username': get_user['username'],
        }
        return res

    @classmethod
    def register(cls, account, password, username, email):
        get_user = cls.user_db.find_one({"account": account})
        get_email = cls.user_db.find_one({"email": email})
        if get_user is not None or get_email is not None:
            return False
        else:
            user_data = [{
                'account': account,
                'password': password,
                'username': username,
                'email': email,
            }, ]
            cls.user_db.insert(user_data)
            return True

    @classmethod
    def get_user_friend_account(cls, account):
        user_info = cls.user_friend_db.find_one({'account': account})
        if user_info is None:
            user_info = [{
                'account': account,
                'friend': no_list(),
            }, ]
            cls.user_friend_db.insert(user_info)
        else:
            return json.loads(user_info['friend'])

    @classmethod
    def get_user_friend(cls, account):
        friend_accounts = cls.get_user_friend_account(account)
        if friend_accounts is not None:
            total_friend = []
            for friend in friend_accounts:
                single_friend_info = cls.user_db.find_one({'account': friend})
                single_friend = {
                    'id': friend,
                    'name': single_friend_info['username']
                }
                total_friend.append(single_friend)
            return total_friend

    @classmethod
    def add_friend(cls, account, other_id):
        has_old_list = cls.get_user_friend_account(account)
        if has_old_list is not None:
            has_old_list.append(other_id)
            cls.user_friend_db.update_one({'account': account}, {'$set': {'friend': json.dumps(has_old_list)}})
        else:
            cls.user_friend_db.update_one({'account': account}, {'$set': {'friend': json.dumps([other_id, ])}})
        return True

    @classmethod
    def user_add_friend(cls, account, other_id):
        owner_add = cls.add_friend(account, other_id)
        friend_add = cls.add_friend(other_id, account)
        if owner_add and friend_add:
            get_user = cls.user_db.find_one({'account': other_id})
            return get_user['username']
        else:
            return False

    @classmethod
    def get_user_group_id(cls, account):
        user_group = cls.user_group_db.find_one({'account': account})
        if user_group is None:
            user_group_data = [{
                'account': account,
                'group_id': no_list(),
            }, ]
            cls.user_group_db.insert(user_group_data)
        else:
            return json.loads(user_group['group_id'])

    @classmethod
    def add_user_group_id(cls, account, group_id):
        user_group = cls.user_group_db.find_one({'account': account})
        if user_group is None:
            user_group_data = [{
                'account': account,
                'group_id': json.dumps([group_id, ]),
            }, ]
            cls.user_group_db.insert(user_group_data)
        else:
            old_list = json.loads(user_group['group_id'])
            old_list.append(group_id)
            cls.user_group_db.update_one({'account': account}, {'$set': {'group_id': json.dumps(old_list)}})

    @classmethod
    def get_user_group(cls, account):
        group_ids = cls.get_user_group_id(account)
        if group_ids is not None:
            total_group = []
            for group_id in group_ids:
                single_group_info = cls.group_db.find_one({'group_id': group_id})
                single_group = {
                    'id': group_id,
                    'name': single_group_info['group_name']
                }
                total_group.append(single_group)
            return total_group

    @classmethod
    def change_user_group(cls, account, user_group_list):
        cls.get_user_group_id(account)
        cls.user_group_db.update_one({'account': account}, {'$set': {'group_id': json.dumps(user_group_list)}})

    @classmethod
    def get_group(cls, group_id):
        group = cls.group_db.find_one({'group_id': group_id})
        if group is not None:
            return json.loads(group['account']), group['group_name']
        else:
            return None, None

    @classmethod
    def change_group(cls, group_id, group_name=None, account=None):
        if group_name is None and account is None:
            return True
        if group_name is not None and account is not None:
            cls.group_db.update_one({'group_id': group_id}, {'$set': {
                'group_name': group_name,
                'account': json.dumps(account),
            }})
        elif group_name is not None:
            cls.group_db.update_one({'group_id': group_id}, {'$set': {
                'group_name': group_name,
            }})
        elif account is not None:
            cls.group_db.update_one({'group_id': group_id}, {'$set': {
                'account': json.dumps(account),
            }})
        return True

    @classmethod
    def create_group(cls, group_name, account):
        this_group_id = str(uuid.uuid4())
        group_data = [{
            'group_id': this_group_id,
            'group_name': group_name,
            'account': json.dumps([account, ]),
        }, ]
        cls.group_db.insert(group_data)
        cls.add_user_group_id(account, this_group_id)
        return this_group_id

    @classmethod
    def get_all_group(cls):
        groups = cls.group_db.find()
        return [group['group_id'] for group in groups]


@check_remote
@get_data
def login(data):
    try:
        res = UserHandler.login(data['account'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    if res is not None:
        status = 'ok'
        data = general_json_data(status, res)
    else:
        status = 'error'
        data = general_json_data(status)
    return web.json_response(data=data)


@check_remote
@get_data
def register(data):
    try:
        register_check = UserHandler.register(
            data['account'],
            data['password'],
            data['username'],
            data['email'],
        )
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    if register_check:
        status = 'ok'
    else:
        status = 'error'
    data = general_json_data(status)
    return web.json_response(data=data)


@check_remote
@get_data
def get_user_info(data):
    try:
        friends = UserHandler.get_user_friend(data['account'])
        groups = UserHandler.get_user_group(data['account'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    res = {}
    if friends:
        res['friend'] = friends
    else:
        res['friend'] = []
    if groups:
        res['group'] = groups
    else:
        res['group'] = []
    res['method'] = 'user_info'
    res_data = general_json_data('ok', res)
    return web.json_response(data=res_data)


@check_remote
@get_data
def get_user_friend(data):
    try:
        res = UserHandler.get_user_friend_account(data['account'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    if res:
        friend = {'friend': res}
    else:
        friend = {'friend': []}
    res_data = general_json_data('ok', friend)
    return web.json_response(data=res_data)


@check_remote
@get_data
def user_add_friend(data):
    try:
        res = UserHandler.user_add_friend(data['account'], data['id'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    if res is not False:
        friend = {'name': res}
        res_data = general_json_data('ok', friend)
        return web.json_response(data=res_data)
    else:
        return error.handle_500()


# @check_remote
# @get_data
# def get_user_group(data):
#     try:
#         res = UserHandler.get_user_group(data['account'])
#     except BaseException as e:
#         UserHandler.Log.exception(e)
#         return error.handle_500()
#     group = {}
#     if res:
#         group = {'group': res}
#     res_data = general_json_data('ok', group)
#     return web.json_response(data=res_data)


@check_remote
@get_data
def user_join_group(data):
    try:
        user_old_group = UserHandler.get_user_group_id(data['account'])
        if user_old_group and data['id'] not in user_old_group:
            user_old_group.append(data['id'])
            UserHandler.change_user_group(data['account'], user_old_group)
        elif not user_old_group:
            new_group = [data['id'], ]
            UserHandler.change_user_group(data['account'], new_group)
        group_old_user, group_name = UserHandler.get_group(data['id'])
        if group_old_user and data['id'] not in group_old_user:
            group_old_user.append(data['account'])
            UserHandler.change_group(data['id'], account=group_old_user)
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    group = {'name': group_name}
    res_data = general_json_data('ok', group)
    return web.json_response(data=res_data)


@check_remote
@get_data
def get_group(data):
    try:
        accounts, group_name = UserHandler.get_group(data['group_id'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    group = {}
    if accounts:
        group = {
            'account': accounts,
            'group_name': group_name,
        }
    res_data = general_json_data('ok', group)
    return web.json_response(data=res_data)


@check_remote
@get_data
def change_group(data):
    try:
        old_accounts, *args = UserHandler.get_group(data['group_id'])
        UserHandler.change_group(data['group_id'], data['group_name'], data['account'])
        if len(old_accounts) > len(data['account']):
            for old_account in old_accounts:
                if old_account not in data['account']:
                    user_old_group = UserHandler.get_user_group(old_account)
                    new_group = user_old_group.remove(data['group_id'])
                    UserHandler.change_user_group(old_account, new_group)
        elif len(old_accounts) > len(data['account']):
            for new_account in data['account']:
                if new_account not in old_accounts:
                    user_group = UserHandler.get_user_group(new_account)
                    if user_group:
                        user_group.append(data['group_id'])
                    else:
                        user_group = [data['group_id'], ]
                    UserHandler.change_user_group(new_account, user_group)
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    return ok_response()


@check_remote
@get_data
def create_group(data):
    try:
        res = UserHandler.create_group(data['name'], data['account'])
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    group = {'id': res}
    res_data = general_json_data('ok', group)
    return web.json_response(data=res_data)


@check_remote
def get_all_group(request):
    try:
        res = UserHandler.get_all_group()
    except BaseException as e:
        UserHandler.Log.exception(e)
        return error.handle_500()
    group = {}
    if res:
        group = {'group_id': res}
    res_data = general_json_data('ok', group)
    return web.json_response(data=res_data)
