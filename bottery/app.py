import asyncio
import importlib
import logging
import logging.config

import aiohttp

from bottery.conf import settings
from bottery.log import DEFAULT_LOGGING

logging.config.dictConfig(DEFAULT_LOGGING)
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
        platforms = settings.PLATFORMS.values()

        # Raise Exception if no platform was configured.
        if not platforms:
            raise Exception('No platform configured')

        # For each platform found on settings.py, create an instance
        # of its engine, run its `configure` method and add its tasks
        # to the App's tasks list. Once it's configured, create
        # a route for its handler.
        for platform in platforms:
            logger.debug('Configuring engine %s', platform['ENGINE'])

            mod = importlib.import_module(platform['ENGINE'])
            platform['OPTIONS']['session'] = self.session
            engine = mod.engine(**platform['OPTIONS'])
            engine.configure()
            tasks = engine.tasks

            if len(tasks):
                self.tasks.append(*tasks)

            logger.debug('[%s] Ready', engine.platform)

    def run(self):
        self.configure_platforms()

        # Add Platforms tasks to the App loop.
        for task in self.tasks:
            self.loop.create_task(task(session=self.session))
        logger.debug('Tasks created')

        self.loop.run_forever()
