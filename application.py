# -*- coding: utf-8 -*-
'''
    application
    ~~~~~~~~~

    app类模块

    内含路由，MongoDB，Redis以及聊天室用户管理类

    :copyright: (c) 2018 by Victor Lai.

'''
import os

import tornado.web
from mongo_app import MongoConn
from redis_app import RedisConn

import view
import config


class Application(tornado.web.Application):

    def __init__(self):
        # favicon.ico 在配置了static_path自动被tornado配置，等级最高，无法由路由规则替换
        handler = [
            tornado.web.url(r'/register', view.index.RegisterHandler, name='register'),
            tornado.web.url(r'/login', view.index.LoginHandler, name='login'),
            tornado.web.url(r'/chat', view.chat.ChatRoomHandler, name='chat'),
            tornado.web.url(r'/chat_room', view.chat.ChatHandler, name='chat_room'),
            tornado.web.url(r'/api/users_message', view.send_message.UsersMessage, name='users_message'),
            tornado.web.url(r'/api/user_message', view.send_message.UserMessage, name='user_message'),
            # 主页使用静态文件，提高处理效率
            (r'/(.*)$', view.index.StaticFileHandler,
             {
                 'path': os.path.join(config.BASE_DIR, 'static/html'),
                 'default_filename': 'index.html'
             }),
        ]
        super(Application, self).__init__(handler, **config.settings)
        self.mongodb = MongoConn(
            config.mongodb['host'],
            config.mongodb['port'],
            config.mongodb['db_name'],
            config.mongodb['username'],
            config.mongodb['password'],

        ).db
        self.redis = RedisConn(
            config.redis['host'],
            config.redis['port'],
            config.redis['password'],
        ).db
