import tornado.web

import view
import config


class Application(tornado.web.Application):

    def __init__(self):
        handler = [
            (r"/", view.index.IndexHandler)
        ]
        super(Application, self).__init__(handler, **config.settings)
