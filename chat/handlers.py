# -*- coding: utf-8 -*-

import json

import tornado.ioloop
import tornado.web
import tornado.websocket

from chat.settings import ANONYMOUS_NICKNAME


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        context = {
            'websocket_url': "ws://{}{}".format(self.request.host,
                                                self.reverse_url('chat'))
        }
        self.render('index.html', **context)


clients = []
global_rooms = {}


class WebSocketChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.nickname = None
        clients.append(self)

    def chat_error(self, message, request):
        self.write_message(json.dumps({
            'action': 'ERROR',
            'request': request,
            'message': message,
        }))

    def chat_response(self, message, request):
        self.write_message(json.dumps({
            'action': 'RESPONSE',
            'request': request,
            'message': message,
        }))

    def chat_login_nick(self, data):
        for client in clients:
            if self is not client and client.nickname == data['nickname']:
                self.chat_error(u'Nickname already in use', data)
                return

        self.nickname = data['nickname']
        self.chat_response(u'OK', data)

    def chat_join_room(self, data):
        room_id = data['room_id']
        if room_id not in global_rooms:
            global_rooms[room_id] = [self]
        else:
            if self not in global_rooms[room_id]:
                global_rooms[room_id].append(self)
            else:
                self.chat_error(u'You are already registered in that room', data)
                return
        self.chat_response(u'OK', data)

    def chat_left_room(self, data):
        room_id = data['room_id']
        if room_id not in global_rooms:
            self.chat_error(u'Room not found', data)
            return
        else:
            if self in global_rooms[room_id]:
                global_rooms[room_id].remove(self)
                if not global_rooms[room_id]:
                    global_rooms.pop(room_id)
            else:
                self.chat_error(u'You are already leave this room', data)
                return
        self.chat_response(u'OK', data)

    def chat_send_message(self, data):
        room_id = data['room_id']
        text = data['text']

        if room_id not in global_rooms or \
                        self not in global_rooms[room_id]:
            self.chat_error(u'You should join this room first', data)
            return

        for client in global_rooms[room_id]:
            client.write_message(json.dumps({
                'action': u'GET MESSAGE',
                'room_id': room_id,
                'author': self.nickname or ANONYMOUS_NICKNAME,
                'text': text,
            }))

    def on_message(self, message):
        try:
            data = json.loads(message)
        except ValueError:
            self.chat_error(u'Unknown message format', message)
            return

        try:
            action = data['action']
        except TypeError:
            self.chat_error(u'Unknown message format', data)
            return
        except ValueError:
            self.chat_error(u'Action is not specified', data)
            return

        if action == u'LOGIN NICK':
            self.chat_login_nick(data)

        elif action == u'JOIN ROOM':
            self.chat_join_room(data)

        elif action == u'LEFT ROOM':
            self.chat_left_room(data)

        elif action == u'SEND MESSAGE':
            self.chat_send_message(data)

        else:
            self.chat_error(u'Action is not supported', data)

    def on_close(self):
        clients.remove(self)

    def check_origin(self, origin):
        return True