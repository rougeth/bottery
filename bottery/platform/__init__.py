import importlib
import logging
import os

from bottery.exceptions import ImproperlyConfigured


logger = logging.getLogger('bottery.platforms')


def discover_and_run_view(message):
    if message is None:
        return None
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise ImproperlyConfigured('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.platform)
            print('Pattern found:', pattern)
            call_view = getattr(pattern, "call_view", None)
            if callable(call_view):
                response = pattern.call_view(message)
                return response
            if isinstance(pattern.view, str):
                view = importlib.import_module(pattern.view)
            else:
                view = pattern.view
            return view(message)

    # raise Exception('No Pattern found!')
    return None


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


class BaseEngine:
    # Should we use ABC for required attributes and methods?

    def __init__(self, **kwargs):
        # For each named parameters received, set it as an instance
        # attribute
        for item, value in kwargs.items():
            setattr(self, item, value)

    @property
    def platform(self):
        """Platform name"""
        raise NotImplementedError('platform attribute not implemented')

    @property
    def tasks(self):
        """List of tasks to be added to the main event loop"""
        raise NotImplementedError('tasks attribute not implemented')

    def build_message(self):
        """
        Build Message instance according to the data received from the
        platform API.
        """
        raise NotImplementedError('build_message not implemented')

    def configure(self):
        """Called by App instance to configure the platform"""
        raise NotImplementedError('configure not implemented')
