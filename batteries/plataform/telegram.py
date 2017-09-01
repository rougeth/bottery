from pprint import pprint

from aiohttp import web

from batteries import plataform
from batteries.conf import settings

import requests


class TelegramEngine(plataform.BasePlataform):
    PLATAFORM = 'telegram'
    API_URL = 'https://api.telegram.org'

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.WEBHOOK_HOST, self.path)

    def configure(self):
        url = '{}/bot{}/setWebhook'.format(self.API_URL, self.token)
        response = requests.post(url, json={'url': self.webhook_url})
        print(response.status_code)

    @property
    def handler(self):
        async def request_handler(request):
            data = await request.json()
            pprint(data)
            return web.Response(text='')

        return request_handler


engine = TelegramEngine
