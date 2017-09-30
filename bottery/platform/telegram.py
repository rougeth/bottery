import logging

import requests

from bottery import platform
from bottery.message import Message
from bottery.user import User

logger = logging.getLogger('bottery.telegram')


def mixed_case(string):
    words = string.split('_')
    return words[0].lower() + ''.join([s.title() for s in words[1:]])


class TelegramAPI:
    api_url = 'https://api.telegram.org'
    methods = [
        'set_webhook',
        'send_message',
    ]

    def __init__(self, token):
        self.token = token

    def make_url(self, method_name):
        method_name = mixed_case(method_name)
        return '{}/bot{}/{}'.format(self.api_url, self.token, method_name)

    def __getattr__(self, attr):
        if attr not in self.methods:
            raise AttributeError

        url = self.make_url(attr)
        return lambda data={}: requests.post(url, json=data)


class TelegramUser(User):
    '''
    Telegram User reference
    https://core.telegram.org/bots/api#user
    '''
    def __init__(self, sender):
        self.id = sender['id']
        self.first_name = sender['first_name']
        self.last_name = sender.get('last_name')
        self.username = sender.get('username')
        self.language = sender.get('language_code')

    def __str__(self):
        s = '{u.first_name}'
        if self.last_name:
            s += ' {u.last_name}'

        s += ' ({u.id})'

        return s.format(u=self)


class TelegramEngine(platform.BasePlataform):
    platform = 'telegram'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = TelegramAPI(self.token)

    def configure(self):
        '''Setup webhook on Telegram'''

        response = self.api.set_webhook({'url': self.webhook_url})
        if response.status_code == 200:
            logger.debug('[%s] Webhook configured', self.platform)
        else:
            logger.warn("[%s] Could not configure webhook url (%s): %s",
                        self.platform,
                        response.status_code,
                        response.json())

    def build_message(self, data):
        '''
        Return a Message instance according to the data received from
        Telegram API.
        https://core.telegram.org/bots/api#update
        '''
        message_data = data.get('message')

        if message_data:
            return Message(
                id=message_data['message_id'],
                platform=self.platform,
                text=message_data['text'],
                user=TelegramUser(message_data['from']),
                timestamp=message_data['date'],
                raw=data,
            )
        else:
            return None

    def handler_response(self, response):
        data = {
            'chat_id': response.chat_id,
            'text': response.text,
        }

        return self.api.send_message(data=data)


engine = TelegramEngine
