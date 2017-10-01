import importlib
import logging
import os

from aiohttp import web

from bottery.conf import settings


logger = logging.getLogger('bottery.platforms')


def discover_view(message):
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise Exception('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.platform)
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
        return '/hook/{}'.format(self.platform)

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.HOSTNAME, self.webhook_endpoint)

    def build_message(self):
        raise NotImplementedError('create_message not implemented')

    def tasks(self):
        return None

    @property
    def handler(self):
        async def handler(request):
            logger.debug('[%s] New message', self.platform)
            data = await request.json()
            logger.debug('[%s] Building message', self.platform)
            message = self.build_message(data)

            if message:
                view = discover_view(message)
                if not view:
                    logger.warn('[%s] Pattern not found for message from %s',
                                message.platform, message.user)
                    return web.Response()
            else:
                logger.warn('Not a message data received, only message data'
                            ' is supported at the moment')
                return web.Response()

            logger.info('[%s] Message from %s', self.platform, message.user)
            response = view(message)
            if isinstance(response, str):
                attrs = {
                    'chat_id': message.user.id,
                    'text': response,
                }
                response = type('Response', (object,), attrs)
                response = self.handler_response(response).json()

                if response['ok']:
                    logger.info('[%s] Response sent to %s', self.platform,
                                message.user)
                else:
                    logger.warn('[%s] Response could not be sent to %s',
                                self.platform, message.user)

            return web.Response()

        return handler
