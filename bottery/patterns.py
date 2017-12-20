from collections import OrderedDict


class BaseHandler:
    def __init__(self, pattern):
        self.pattern = pattern

    def check(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithHandler(BaseHandler):
    def check(self, message):
        if message.text.startswith(self.pattern):
            return True
        return False


class DefaultHandler:
    def check(self, message):
        return True


class PatternsHandler:
    def __init__(self):
        self.registered = OrderedDict()

    def register(self, handler, pattern, view):
        if not self.registered.get(handler.__name__):
            self.registered[handler.__name__] = (handler(pattern), view)

    def __call__(self, pattern):
        def decorator(view):
            self.register(BaseHandler, pattern, view)
            return view

        return decorator

    def startswith(self, pattern):
        def decorator(view):
            self.register(StartswithHandler, pattern, view)
            return view

        return decorator

    def default(self):
        def decorator(view):
            self.register(DefaultHandler, None, view)
            return view

        return decorator
