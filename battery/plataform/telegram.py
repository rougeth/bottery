import logging
from datetime import datetime

from battery import plataform
from battery.conf import settings
from battery.message import Message
from battery.user import User

import requests


logger = logging.getLogger('battery.telegram')


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
        def request(data={}):
            return requests.post(url, json=data)

        return request


class TelegramUser(User):

    @classmethod
    def from_telegram(cls, sender):
        '''
        Returns a TelegramUser instance based on the data received from
        Telegram API.
        https://core.telegram.org/bots/api#user
        '''
        return cls(
            id=sender['id'],
            first_name=sender['first_name'],
            last_name=sender['last_name'],
            username=sender['username'],
            language=sender['language_code'])

    def __str__(self):
        s = '({u.id}) {u.first_name}'
        if self.last_name:
            s += ' {u.last_name}'

        return s.format(u=self)


class TelegramEngine(plataform.BasePlataform):
    plataform = 'telegram'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = TelegramAPI(self.token)

    def configure(self):
        '''Setup webhook on Telegram'''

        response = self.api.set_webhook({'url': self.webhook_url})
        if response.status_code == 200:
            logger.debug('[%s] Webhook configured', self.plataform)
        else:
            logger.warn("[%s] Could not configure webhook url (%s): %s",
                        self.plataform,
                        response.status_code,
                        response.json())

    def build_message(self, data):
        '''
        Return a Message instance according to the data received from
        Telegram API.
        https://core.telegram.org/bots/api#update
        '''
        return Message(
            id=data['message']['message_id'],
            plataform=self.plataform,
            text=data['message']['text'],
            user=TelegramUser.from_telegram(data['message']['from']),
            timestamp=data['message']['date'],
            raw=data,
        )

    def handler_response(self, response):
        data = {
            'chat_id': response.chat_id,
            'text': response.text,
        }

        return self.api.send_message(data=data)

engine = TelegramEngine
