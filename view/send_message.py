# -*- coding: utf-8 -*-
import json

from tornado.web import RequestHandler

from utils import set_logging
from view.utils import ChatUser
import config


class Log:
    logger = set_logging('sender.')


class UsersMessage(RequestHandler):

    users = ChatUser.users

    def send_data_to_users(self, account: list, data):
        Log.logger.info('群发信息目标帐号: ' + str(account) + ' 群发信息: ' + str(data))
        print([x.account for x in self.users])
        for user in self.users:
            if user.account in account:
                user.write_message(json.dumps(data))

    def post(self):
        if self.request.remote_ip in config.trust_list:
            json_data = json.loads(self.request.body)
            self.send_data_to_users(json_data['g_id'], json_data)
            self.write('ok')
        else:
            self.write('error')

    def check_xsrf_cookie(self):
        pass


class UserMessage(RequestHandler):

    users = ChatUser.users

    def send_data_to_user(self, account, data):
        Log.logger.info('单发信息目标帐号: ' + str(account) + ' 单发信息: ' + str(data))
        for user in self.users:
            if user.account == account:
                return user.write_message(json.dumps(data))

    def post(self):
        if self.request.remote_ip in config.trust_list:
            json_data = json.loads(self.request.body)
            self.send_data_to_user(json_data['g_id'], json_data)
            self.write('ok')
        else:
            self.write('error')

    def check_xsrf_cookie(self):
        pass
