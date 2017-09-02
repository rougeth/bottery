import logging

from aiohttp import web

WEBHOOK_PATH = '/hook/'


logger = logging.getLogger('batteries.server')


async def handler(request):
    logger.debug('New request')
    return web.Response(text='batteries')
