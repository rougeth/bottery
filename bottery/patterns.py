from .handlers import (DefaultHandler, MessageHandler, RegexHandler,
                       StartswithHandler)


class Patterns:
    def __init__(self):
        self.registered = []

    def register(self, handler, view, pattern=None, *args, **kwargs):
        self.registered.append((handler(pattern, *args, **kwargs), view))

    def message(self, pattern, case_sensitive=True):
        def decorator(view):
            self.register(MessageHandler, view, pattern, case_sensitive)
            return view

        return decorator

    def startswith(self, pattern, case_sensitive=True):
        def decorator(view):
            self.register(StartswithHandler, view, pattern, case_sensitive)
            return view

        return decorator

    def default(self):
        def decorator(view):
            self.register(DefaultHandler, view)
            return view

        return decorator

    def regex(self, pattern):
        def decorator(view):
            self.register(RegexHandler, view, pattern)
            return view

        return decorator
