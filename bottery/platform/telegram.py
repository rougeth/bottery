import asyncio
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
        'delete_webhook',
        'send_message',
        'set_webhook',
        'get_updates',
    ]

    def __init__(self, token, session=None):
        self.token = token
        self.session = session

    def make_url(self, method_name):
        method_name = mixed_case(method_name)
        return '{}/bot{}/{}'.format(self.api_url, self.token, method_name)

    @property
    def http_client(self):
        return self.session or requests

    def __getattr__(self, attr):
        if attr not in self.methods:
            raise AttributeError('FUCK')

        url = self.make_url(attr)
        return lambda data={}: self.http_client.post(url, json=data)


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

        # If no `mode` was defined at settings.py, use by default
        # polling mode.
        if not hasattr(self, 'mode'):
            self.mode = 'polling'

    def configure_polling(self):
        response = self.api.delete_webhook()
        response = response.json()
        if response['ok']:
            logger.debug('[%s] Polling mode set', self.platform)

    def configure_webhook(self):
        response = self.api.set_webhook({'url': self.webhook_url})
        if response.status_code == 200:
            logger.debug('[%s] Webhook mode set', self.platform)
        else:
            logger.warn("[%s] Could not configure webhook url (%s): %s",
                        self.platform,
                        response.status_code,
                        response.json())

    def configure(self):
        if self.mode == 'webhook':
            self.configure_webhook()
        else:
            self.configure_polling()

        self.api.session = self.session

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

    def tasks(self):
        return [self.polling]

    async def polling(self, session, last_update=None):
        payload = {}
        if last_update:
            # `offset` param prevets from getting duplicates updates
            # from Telegram API:
            # https://core.telegram.org/bots/api#getupdates
            payload['offset'] = last_update + 1


        response = await self.api.get_updates(payload)
        updates = await response.json()

        for update in updates['result']:
            logger.debug('[%s] New message', self.platform)

        if len(updates['result']):
            last_update = updates['result'][-1]['update_id']

        await asyncio.sleep(1)
        await self.polling(session, last_update)


engine = TelegramEngine
