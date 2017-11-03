import asyncio
import importlib
import logging
import logging.config
from datetime import datetime

import aiohttp
import click
from halo import Halo

import bottery
from bottery.conf import settings

logger = logging.getLogger('bottery')


class App:

    _loop = None
    _session = None
    _configure = None
    tasks = []

    @property
    def session(self):
        if not self._session:
            self._session = aiohttp.ClientSession(loop=self.loop)
        return self._session

    @property
    def loop(self):
        if not self._loop:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def configure_platforms(self):
        platforms = settings.PLATFORMS.items()

        # Raise Exception if no platform was configured.
        if not platforms:
            raise Exception('No platform configured')

        # For each platform found on settings.py, create an instance
        # of its engine, run its `configure` method and add its tasks
        # to the App's tasks list. Once it's configured, create
        # a route for its handler.
        for engine_name, platform in platforms:
            spinner_msg = 'Configuring %s' % engine_name
            with Halo(text=spinner_msg, spinner='dots') as spinner:
                mod = importlib.import_module(platform['ENGINE'])
                platform['OPTIONS']['engine_name'] = engine_name
                platform['OPTIONS']['session'] = self.session
                engine = mod.engine(**platform['OPTIONS'])
                engine.configure()
                tasks = engine.tasks

                if len(tasks):
                    self.tasks.extend(tasks)
                spinner_msg = '{} configured'.format(engine_name).capitalize()
                spinner.succeed(spinner_msg)

        click.echo()  # Just print an empty line

    def run(self):
        self.configure_platforms()

        # Add Platforms tasks to the App loop.
        for task in self.tasks:
            self.loop.create_task(task(session=self.session))

        now = datetime.now().strftime('%B %d, %Y - %X')
        msg = ('{now}\n'
               'Bottery version {version}\n'
               'Starting development server\n'
               'Quit the server with CONTROL-C\n')
        click.echo(msg.format(now=now, version=bottery.__version__))
        self.loop.run_forever()

    def stop(self):
        self.session.close()
        # Exit event loop at the next suitable opportunity...
        self.loop.stop()
        # ...and now close it.
        self.loop.close()
