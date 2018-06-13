# -*- coding: utf-8 -*-
import datetime
import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

import config


class ChatRoomHandler(RequestHandler):

    def get(self):
        user_token = self.get_secure_cookie("user_token")
        chat_room_user = self.get_secure_cookie("chat_room_user")
        if self.application.redis.hexists("user_token", chat_room_user):
            get_token = self.application.redis.hget("user_token", chat_room_user)
            if str(user_token)[2:-1] == str(get_token):
                chat_url = "ws://" + config.settings['local_url'] + ":" + str(config.options['port']) + RequestHandler.reverse_url(self, "chat_room")
                return self.render("chat/chat_room.html", chat_url=chat_url, user_token=user_token)
        url = RequestHandler.reverse_url(self, "login")
        return self.redirect(url)


class ChatHandler(WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        self.users = self.application.chat_room.user  # 用来存放在线用户的容器
        self.username = str(self.get_secure_cookie("chat_room_username"))[2:-1]
        self.account = str(self.get_secure_cookie("chat_room_user"))[2:-1]

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        now_user = "当前在线用户："
        for u in self.users:  # 向已在线用户发送消息
            msg_str = u"[%s]-[%s]-进入大厅" % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg_json = json.dumps({"info": "info", "msg": msg_str})
            u.write_message(msg_json)
            if len(now_user) < 20:
                now_user += u.username
                now_user += "，"
            elif len(now_user) == 20:
                now_user += "..."
        if now_user[-1] == "，":
            now_user = now_user[:-1]
        for u in self.users:
            now_user_json = json.dumps({"info": "now_user", "msg": now_user})
            u.write_message(now_user_json)
        if not self.application.redis.hexists("user_token", self.account):
            self.application.redis.hset("user_token", self.account, str(self.get_secure_cookie("user_token"))[2:-1])

    def on_message(self, message):
        message = json.loads(message)
        if message['user']:
            chat_to_user = False
            for u in self.users:  # 向指定用户广播消息
                if u == self:
                    msg_str = u"[你]-[%s]-悄悄对%s说：%s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['user'], message['msg'])
                    msg_json = json.dumps({"info": "info", "msg": msg_str})
                    u.write_message(msg_json)
                elif u.username == message['user']:
                    chat_to_user = True
                    msg_str = u"[%s]-[%s]-悄悄对你说：%s" % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['msg'])
                    msg_json = json.dumps({"info": "info", "msg": msg_str})
                    u.write_message(msg_json)
            if not chat_to_user:
                msg_str = "该用户没有在线，发送失败"
                msg_json = json.dumps({"info": "info", "msg": msg_str})
                self.write_message(msg_json)
        else:
            for u in self.users:  # 向在线用户广播消息
                msg_str = u"[%s]-[%s]-说：%s" % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message['msg'])
                msg_json = json.dumps({"info": "info", "msg": msg_str})
                u.write_message(msg_json)

    def on_close(self):
        self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        self.application.redis.hdel("user_token", self.account)
        now_user = "当前在线用户："
        for u in self.users:
            msg_str = u"[%s]-[%s]-离开大厅" % (self.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg_json = json.dumps({"info": "info", "msg": msg_str})
            u.write_message(msg_json)
            if len(now_user) < 20:
                now_user += u.username
                now_user += "，"
            elif len(now_user) == 20:
                now_user += "..."
        if now_user[-1] == "，":
            now_user = now_user[:-1]
        for u in self.users:
            now_user_json = json.dumps({"info": "now_user", "msg": now_user})
            u.write_message(now_user_json)

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
