import asyncio
import importlib

import aiohttp

from bottery.cli import cli
from bottery.conf import Settings
from bottery.patterns import PatternsHandler


class Bottery:
    _loop = None
    _session = None
    _server = None
    patterns = PatternsHandler()
    cli = cli

    def __init__(self, settings_module='settings'):
        self.settings = Settings.from_object(settings_module)
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

    async def configure_engine(self, engine):
        await engine.configure()
        self.tasks.extend(engine.tasks)

    async def configure(self):
        platforms = self.settings.PLATFORMS.items()
        if not platforms:
            raise Exception('No platforms configured')

        global_options = {
            'loop': self.loop,
            'session': self.session,
            'registered_patterns': self.patterns.registered,
        }

        config_tasks = []
        for engine_name, platform in platforms:
            if not platform.get('OPTIONS'):
                platform['OPTIONS'] = {}
            platform['OPTIONS'].update(global_options)

            try:
                mod = importlib.import_module(platform['ENGINE'])
            except ImportError:
                # TODO: log
                continue

            engine = mod.engine(**platform['OPTIONS'])
            config_tasks.append(self.configure_engine(engine))

        await asyncio.gather(*config_tasks)

    def run(self):
        self.loop.run_until_complete(self.configure())

        if not self.tasks:
            return

        for task in self.tasks:
            self.loop.create_task(task())

        self.loop.run_forever()

    def stop(self):
        self.session.close()
        self.loop.close()
