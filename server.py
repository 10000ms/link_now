import tornado.ioloop
import tornado.httpserver

import config
import application


if __name__ == "__main__":
    app = application.Application()
    app.listen(config.options["port"])
    tornado.ioloop.IOLoop.current().start()
