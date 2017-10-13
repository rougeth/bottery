import importlib
import logging
import os

from bottery.conf import settings
from bottery.exceptions import ImproperlyConfigured


logger = logging.getLogger('bottery.platforms')


def discover_view(message):
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise ImproperlyConfigured('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.platform)
            if isinstance(pattern.view, str):
                return importlib.import_module(pattern.view)
            return pattern.view

    # raise Exception('No Pattern found!')
    return None


class BasePlatform:

    def __init__(self, **kw):
        self.tasks = []

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
