import importlib
import logging
import os

from aiohttp import web

from bottery.conf import settings


logger = logging.getLogger('bottery.plataforms')


def discover_view(message):
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise Exception('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.plataform)
            if isinstance(pattern.view, str):
                return importlib.import_module(pattern.view)
            return pattern.view

    # raise Exception('No Pattern found!')
    return None


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
            view = discover_view(message)
            if not view:
                logger.warn('[%s] Pattern not found for message from %s',
                            message.plataform, message.user)
                return web.Response()

            logger.info('[%s] Message from %s', self.plataform, message.user)
            response = view(message)
            if isinstance(response, str):
                attrs = {
                    'chat_id': message.user.id,
                    'text': response,
                }
                response = type('Response', (object,), attrs)
                response = self.handler_response(response).json()

                if response['ok']:
                    logger.info('[%s] Response sent to %s', self.plataform,
                                message.user)
                else:
                    logger.warn('[%s] Response could not be sent to %s',
                                self.plataform, message.user)

            return web.Response()

        return handler
