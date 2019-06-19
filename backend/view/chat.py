# -*- coding: utf-8 -*-
"""
    chat
    ~~~~~~~~~

    聊天室页面及聊天室处理的WebSocket


    :copyright: (c) 2018 by Victor Lai.

"""
import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

import config
from utils import (
    get_redis_fetch_data,
    get_mongo_fetch_data,
    set_logging,
)
from view.utils import ChatUser


class ChatRoomHandler(RequestHandler):

    async def get(self):
        """
        聊天室页面get方法
        :return: 检查通过的用户返回聊天室页面，错误返回登陆页面
        """
        user_token = self.get_secure_cookie('user_token').decode()
        account = self.get_secure_cookie('account').decode()
        username = self.get_secure_cookie('chat_room_username').decode()

        # 检查用户cookie信息是否和Redis数据库中的一致
        session_check_data = {
            'account': account,
            'session': user_token,
            'remote': 'http://{}'.format(config.internal_host),
        }
        res = await get_redis_fetch_data(session_check_data, '/session/check_session')
        status = json.loads(res)
        status = status['status']
        if status == 'ok':
            # 生成聊天室WebSocket地址
            # 因为暂时不使用分布式，所以聊天室地址固定为和web app一个地址
            chat_url = 'ws://{}{}'.format(self.request.host, RequestHandler.reverse_url(self, 'chat_room'))
            return self.render('chat/chat_room.html', chat_url=chat_url, account=account, username=username)
        else:
            url = RequestHandler.reverse_url(self, 'login')
            return self.redirect(url)


class ChatHandler(WebSocketHandler):

    users = ChatUser.users
    logger = set_logging('server.')

    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        # 用来存放在线用户的容器s
        self.username = self.get_secure_cookie('chat_room_username').decode()
        self.account = self.get_secure_cookie('account').decode()

    async def open(self):
        """
        当用户建立连接时，把当前连接类添加到聊天室用户管理类，并向当前在线用户广播新用户加入及当前在线用户
        :return: JSON信息数据
        """
        self.logger.info('open_websocket: ' + self.account)
        # 建立连接后添加用户到容器中
        self.users.add(self)
        # 发送用户上线数据
        json_redis_data = {
            'account': self.account,
            'username': self.username,
        }
        await get_redis_fetch_data(json_redis_data, '/message/user_login')
        # 获取远程的用户数据
        json_mongo_data = {
            'account': self.account,
        }
        res = await get_mongo_fetch_data(json_mongo_data, '/user/get_user_info')
        self.write_message(res)

    async def on_message(self, message):
        """
        当用户发送信息时，向指定用户或者大厅发送信息
        :param message: JSON信息数据
        :return: JSON信息数据
        """
        self.logger.info('message_websocket: ' + self.account + str(message))
        # 加载JSON信息
        message = json.loads(message)
        # 普通信息
        if message['method'] == 'message':
            message_data = {
                'account': self.account,
                'name': self.username,
            }
            message.update(message_data)
            await get_redis_fetch_data(message, '/message/add')
        # 添加好友
        elif message['method'] == 'add_friend':
            message_data = {
                'account': self.account,
                'id': message['id'],
                'name': self.username
            }
            await get_redis_fetch_data(message_data, '/message/add_friend')
        # 添加群
        elif message['method'] == 'add_group':
            message_data = {
                'account': self.account,
                'id': message['id'],
                'name': self.username
            }
            await get_redis_fetch_data(message_data, '/message/add_group')
        # 创建群
        elif message['method'] == 'create_group':
            message_data = {
                'account': self.account,
                'name': message['name'],
            }
            await get_redis_fetch_data(message_data, '/message/create_group')

    async def on_close(self):
        self.logger.info('close_websocket: ' + self.account)
        # 用户关闭连接后从容器中移除用户
        self.users.remove(self)
        # 发送用户离线数据
        json_redis_data = {
            'account': self.account,
            'username': self.username
        }
        await get_redis_fetch_data(json_redis_data, '/message/user_logout')

    def check_origin(self, origin):
        # 允许WebSocket的跨域请求
        return True

    async def on_connection_close(self):
        # 改写此方法，使on_close可以被异步调用
        if self.ws_connection:
            self.ws_connection.on_connection_close()
            self.ws_connection = None
        if not self._on_close_called:
            self._on_close_called = True
            await self.on_close()
            self._break_cycles()

