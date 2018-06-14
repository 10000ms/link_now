# -*- coding: utf-8 -*-
"""
    server
    ~~~~~~~~~

    项目入口及启动模块

    :copyright: (c) 2018 by Victor Lai.

"""
import tornado.ioloop
import tornado.httpserver

import config
import application


if __name__ == "__main__":
    app = application.Application()
    app.listen(config.options["port"])
    tornado.ioloop.IOLoop.current().start()
