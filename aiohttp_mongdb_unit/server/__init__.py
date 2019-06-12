#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aiohttp import web

from config import config
from server.route import route
from server.utils import ServerComponent


def print_to_logging(*args, **kwargs):
    string = ' '.join(args)
    ServerComponent.logger.info(string)


def main():
    app = web.Application()
    app.add_routes(route())
    new_logger = ServerComponent.logger
    if not config.SERVER_CONFIG:
        server_config = {
            'host': '127.0.0.1',
            'port': '8091',
        }
    else:
        server_config = config.SERVER_CONFIG
    new_logger.info('服务器启动:' + server_config['host'] + ':' + server_config['port'])
    web.run_app(app, print=print_to_logging, access_log=new_logger, **server_config)


if __name__ == '__main__':
    main()
