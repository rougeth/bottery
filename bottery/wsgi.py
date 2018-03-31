from aiohttp import GunicornWebWorker  # noqa

from bottery import Bottery


def get_wsgi_application():
    bot = Bottery()
    bot.configure()
    return bot.server
