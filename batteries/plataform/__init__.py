import logging

from aiohttp import web

from batteries.conf import settings



logger = logging.getLogger('batteries.plataforms')


class BasePlataform:

    def __init__(self, **kw):
        for item, value in kw.items():
            setattr(self, item, value)

    @property
    def webhook_endpoint(self):
        return '/hook/{}'.format(self.plataform)

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.HOSTNAME, self.webhook_endpoint)

    def build_message(self):
        raise NotImplementedError('create_message not implemented')

    @property
    def handler(self):
        async def handler(request):
            logger.debug('[%s] New message', self.plataform)
            data = await request.json()
            logger.debug('[%s] Building message', self.plataform)
            message = self.build_message(data)
            logger.info('[%s] Message from %s', self.plataform, message.sender)
            return web.Response(text='batteries')

        return handler
