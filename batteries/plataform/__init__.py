import logging

from aiohttp import web

from batteries import server
from batteries.conf import settings



logger = logging.getLogger('batteries.plataforms')


class BasePlataform:

    def __init__(self, **kw):
        for item, value in kw.items():
            setattr(self, item, value)

    @property
    def handler(self):
        raise NotImplementedError('handler property not implemented')

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.HOSTNAME, server.WEBHOOK_PATH)

    def create_message(self):
        raise NotImplementedError('create_message not implemented')
