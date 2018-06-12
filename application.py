# -*- coding: utf-8 -*-
import os

import tornado.web
from mongo_app import MongoConn

import view
import config


class Application(tornado.web.Application):

    def __init__(self):
        handler = [
            tornado.web.url(r"/register", view.index.RegisterHandler, name="register"),
            tornado.web.url(r"/login", view.index.LoginHandler, name="login"),
            (r"/(.*)$", view.index.StaticFileHandler,
             {
                 "path": os.path.join(config.BASE_DIR, "static/html"),
                 "default_filename": "index.html"
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
