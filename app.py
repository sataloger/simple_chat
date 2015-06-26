# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket

from chat import settings
from chat.handlers import IndexHandler, WebSocketChatHandler


class ChatApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            tornado.web.url(r'/chat', WebSocketChatHandler, name='chat'),
            tornado.web.url(r'/', IndexHandler, name='index')
        ]
        settings_data = {
            "template_path": settings.TEMPLATE_PATH,
            "static_path": settings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings_data)


def main():
    app = ChatApplication()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
