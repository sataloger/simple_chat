## Server supports next actions:


**'LOGIN NICK'** <br />
Allows you to change your nickname in chat to custom one. New nickname should be unique.

Params:

    'nickname' - new nickname [string]

Example: {

    'action': 'LOGIN NICK',
    'nickname': 'Bob'
}

**'JOIN ROOM'** <br />
Subscribe to new messages in selected room. If room does not exist, then it will be created. <br />
Params:

    'room_id' - room identifier [int or string]

Example: {

    'action': 'JOIN ROOM',
    'room_id': 'secret'
}

**'LEFT ROOM'** <br />
Unsubscribe from new messages in selected room. If room is empty, it will be removed. <br />
Params:

    'room_id' - room identifier [int or string]

Example: {

    'action': 'LEFT ROOM',
    'room_id': 'flood'
}

**'SEND MESSAGE'** <br />
Sends a message to selected room. <br />
Params:

    'room_id' - room identifier [int or string]
    'text' - message text [string]

Example: {

    'action': 'SEND MESSAGE',
    'room_id': room_id,
    'text': message
}

## Server sends to client next actions:

**'RESPONSE'** <br />
Requested command was successfully handled. <br />
Params:

    'request' - dict with successful request (same as described at server actions section) [dict]
    'message' - response message text. Commonly "OK" [string]

Example: {

    'action': 'RESPONSE',
    'request': {
        'action': 'JOIN ROOM',
        'room_id': 'secret'
    },
    'message': 'OK',
}

**'ERROR'** <br />
An error occured while processing requested command. <br />
Params:

    'request' - dict with failed request (same as described at server actions section) [dict]
    'message' - error message text. [string]

Example: {

    'action': 'ERROR',
    'request': {
        'action': 'LOGIN NICK',
        'nickname': 'Bob'
    },
    'message': 'Nickname already in use',
}

**'GET MESSAGE'** <br />
Recived message from one of rooms client subscribed on. <br />
Params:

    'room_id' - room identifier [int or string]
    'author' - message author [string]
    'text' - message text [string]

Example: {

    'action': u'GET MESSAGE',
    'room_id': 'secret',
    'author': 'Alice',
    'text': 'What I've done?',
}
