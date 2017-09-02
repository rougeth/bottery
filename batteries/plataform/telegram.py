import logging

from aiohttp import web

from batteries import plataform
from batteries.conf import settings

import requests


logger = logging.getLogger('batteries.telegram')


class TelegramEngine(plataform.BasePlataform):
    PLATAFORM = 'telegram'
    API_URL = 'https://api.telegram.org'

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.HOSTNAME, self.path)

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

    @property
    def handler(self):
        async def request_handler(request):
            data = await request.json()
            logger.info('[%s] new message from %s', self.PLATAFORM,
                        data['message']['from']['username'])
            return web.Response(text='')

        return request_handler


engine = TelegramEngine
