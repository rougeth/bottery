import asyncio
import importlib
import sys
from datetime import datetime

import aiohttp.web
import click

import bottery
from bottery.conf import settings
from bottery.log import Spinner


class Bottery:
    _loop = None
    _session = None
    _server = None

    def __init__(self, settings_module='settings'):
        self.tasks = []

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self.loop)
        return self._session

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    @property
    def server(self):
        if self._server is None:
            self._server = aiohttp.web.Application()
        return self._server

    def get_msghandlers(self):
        # TODO: module `handlers` should be configurable on settings.py
        try:
            return importlib.import_module('handlers').msghandlers
        except ImportError:
            raise Exception("'handlers' module not found!")
        except AttributeError:
            raise Exception("'msghandlers' not found!")

    async def configure(self):
        platforms = settings.PLATFORMS.items()
        if not platforms:
            raise Exception('No platforms configured')

        global_options = {
            'loop': self.loop,
            'session': self.session,
            'server': self.server,
            'registered_handlers': self.get_msghandlers(),
            'settings': settings,
        }

        for engine_name, platform in platforms:
            if not platform.get('OPTIONS'):
                platform['OPTIONS'] = {}
            platform['OPTIONS'].update(global_options)
            platform['OPTIONS']['engine_name'] = engine_name

            try:
                mod = importlib.import_module(platform['ENGINE'])
            except ImportError:
                # TODO: log
                continue

            with Spinner('Configuring %s' % engine_name.title()):
                engine = mod.engine(**platform['OPTIONS'])
                await engine.configure()
                self.tasks.extend(engine.tasks)

    def run(self, server_port):
        click.echo('{now}\n{bottery} version {version}'.format(
            now=datetime.now().strftime('%B %d, %Y -  %H:%M:%S'),
            bottery=click.style('Bottery', fg='green'),
            version=bottery.__version__
        ))

        self.loop.run_until_complete(self.configure())

        if self._server is not None:
            handler = self.server.make_handler()
            setup_server = self.loop.create_server(handler, '0.0.0.0',
                                                   server_port)
            self.loop.run_until_complete(setup_server)
            click.echo('Server running at http://localhost:{port}'.format(
                port=server_port
            ))

        if not self.tasks:
            click.secho('No tasks found.', fg='red')
            self.stop()
            sys.exit(1)

        for task in self.tasks:
            self.loop.create_task(task())

        click.echo('Quit the bot with CONTROL-C')
        self.loop.run_forever()

    def stop(self):
        self.session.close()
        self.loop.close()
