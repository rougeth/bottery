import logging
from datetime import datetime

from batteries import plataform
from batteries.conf import settings
from batteries.message import Message
from batteries.user import User

import requests


logger = logging.getLogger('batteries.telegram')


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
    api_url = 'https://api.telegram.org'

    def configure(self):
        '''Setup webhook on Telegram'''

        url = '{}/bot{}/setWebhook'.format(self.api_url, self.token)
        response = requests.post(url, json={'url': self.webhook_url})
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
            plataform=self.plataform,
            text=data['message']['text'],
            sender=TelegramUser.from_telegram(data['message']['from']),
            timestamp=data['message']['date'],
            raw=data,
        )


engine = TelegramEngine
