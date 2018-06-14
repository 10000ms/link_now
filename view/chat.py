# -*- coding: utf-8 -*-
"""
    chat
    ~~~~~~~~~

    聊天室页面及聊天室处理的WebSocket


    :copyright: (c) 2018 by Victor Lai.

"""
import datetime
import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

import config


class ChatRoomHandler(RequestHandler):

    def get(self):
        """
        聊天室页面get方法
        :return: 检查通过的用户返回聊天室页面，错误返回登陆页面
        """
        user_token = self.get_secure_cookie("user_token")
        chat_room_user = self.get_secure_cookie("chat_room_user")
        # 检查用户cookie信息是否和Redis数据库中的一致
        if self.application.redis.hexists("user_token", chat_room_user):
            get_token = self.application.redis.hget("user_token", chat_room_user)
            if str(user_token)[2:-1] == str(get_token):
                # 生成聊天室WebSocket地址
                chat_url = "ws://" + config.settings['local_url'] \
                           + ":" + str(config.options['port']) \
                           + RequestHandler.reverse_url(self, "chat_room")
                return self.render("chat/chat_room.html", chat_url=chat_url, user_token=user_token)
        url = RequestHandler.reverse_url(self, "login")
        return self.redirect(url)


class ChatHandler(WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        # 用来存放在线用户的容器
        self.users = self.application.chat_room.user
        self.username = str(self.get_secure_cookie("chat_room_username"))[2:-1]
        self.account = str(self.get_secure_cookie("chat_room_user"))[2:-1]

    def open(self):
        """
        当用户建立连接时，把当前连接类添加到聊天室用户管理类，并向当前在线用户广播新用户加入及当前在线用户
        :return: JSON信息数据
        """
        # 建立连接后添加用户到容器中
        self.users.add(self)
        now_user = "当前在线用户："
        # 先广播用户加入，并记录当前在线用户
        for u in self.users:
            msg_str = u"[%s]-[%s]-进入大厅" \
                      % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg_json = json.dumps({"info": "info", "msg": msg_str})
            u.write_message(msg_json)
            # 超过20个后不再记录
            if len(now_user) < 20:
                now_user += u.username
                now_user += "，"
            elif len(now_user) == 20:
                now_user += "..."
        # 去除最后一个逗号
        if now_user[-1] == "，":
            now_user = now_user[:-1]
        # 广播当前在线用户
        for u in self.users:
            now_user_json = json.dumps({"info": "now_user", "msg": now_user})
            u.write_message(now_user_json)
        if not self.application.redis.hexists("user_token", self.account):
            self.application.redis.hset("user_token", self.account, str(self.get_secure_cookie("user_token"))[2:-1])

    def on_message(self, message):
        """
        当用户发送信息时，向指定用户或者大厅发送信息
        :param message: JSON信息数据
        :return: JSON信息数据
        """
        # 加载JSON信息
        message = json.loads(message)
        # 判断是否是向单独用户发送信息
        if message['user']:
            # 记录是否有该用户
            chat_to_user = False
            # 循环用户管理类，找到指定用户
            for u in self.users:
                # 向自己广播发送的信息
                if u == self:
                    msg_str = u"[你]-[%s]-悄悄对%s说：%s" \
                              % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['user'], message['msg'])
                    msg_json = json.dumps({"info": "info", "msg": msg_str})
                    u.write_message(msg_json)
                # 向指定用户广播消息
                elif u.username == message['user']:
                    # 已找到指定用户
                    chat_to_user = True
                    msg_str = u"[%s]-[%s]-悄悄对你说：%s" \
                              % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['msg'])
                    msg_json = json.dumps({"info": "info", "msg": msg_str})
                    u.write_message(msg_json)
            # 若无指定用户
            if not chat_to_user:
                msg_str = "该用户没有在线，发送失败"
                msg_json = json.dumps({"info": "info", "msg": msg_str})
                self.write_message(msg_json)
        else:
            # 若无指定用户，则向全体用户广播
            for u in self.users:
                msg_str = u"[%s]-[%s]-说：%s" \
                          % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['msg'])
                msg_json = json.dumps({"info": "info", "msg": msg_str})
                u.write_message(msg_json)

    def on_close(self):
        # 用户关闭连接后从容器中移除用户
        self.users.remove(self)
        # 从Redis中移除登陆用户token记录
        self.application.redis.hdel("user_token", self.account)
        now_user = "当前在线用户："
        # 向当前在线用户广播，并记录当前在线用户
        for u in self.users:
            msg_str = u"[%s]-[%s]-离开大厅" \
                      % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg_json = json.dumps({"info": "info", "msg": msg_str})
            u.write_message(msg_json)
            # 超过20个后不再记录
            if len(now_user) < 20:
                now_user += u.username
                now_user += "，"
            elif len(now_user) == 20:
                now_user += "..."
        # 去除最后一个逗号
        if now_user[-1] == "，":
            now_user = now_user[:-1]
        # 广播当前在线用户
        for u in self.users:
            now_user_json = json.dumps({"info": "now_user", "msg": now_user})
            u.write_message(now_user_json)

    def check_origin(self, origin):
        # 允许WebSocket的跨域请求
        return True
