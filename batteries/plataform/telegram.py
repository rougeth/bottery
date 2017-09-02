import logging
from datetime import datetime

from batteries import plataform
from batteries.conf import settings
from batteries.message import Message

import requests


logger = logging.getLogger('batteries.telegram')


class TelegramEngine(plataform.BasePlataform):
    PLATAFORM = 'telegram'
    API_URL = 'https://api.telegram.org'

    def configure(self):
        '''Setup webhook on Telegram'''

        url = '{}/bot{}/setWebhook'.format(self.API_URL, self.token)
        response = requests.post(url, json={'url': self.webhook_url})
        if response.status_code == 200:
            logger.debug('[%s] Webhook configured', self.PLATAFORM)
        else:
            logger.warn("[%s] Could not configure webhook url (%s): %s",
                        self.PLATAFORM,
                        response.status_code,
                        response.json())

    def create_message(self, data):
        return Message(
            plataform=self.PLATAFORM,
            text=data['message']['text'],
            sender=data['message']['from'],
            timestamp=data['message']['date'],
            raw=data,
        )


engine = TelegramEngine
