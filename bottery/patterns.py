class BaseHandler:
    def __init__(self, pattern=None):
        self.pattern = pattern

    def check(self, message):
        raise Exception('check method not implemented')


class MessageHandler(BaseHandler):
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
        self.registered = []

    def register(self, handler, view, pattern=None, *args, **kwargs):
        self.registered.append((handler(pattern, *args, **kwargs), view))

    def message(self, pattern):
        def decorator(view):
            self.register(MessageHandler, view, pattern)
            return view

        return decorator

    def startswith(self, pattern):
        def decorator(view):
            self.register(StartswithHandler, view, pattern)
            return view

        return decorator

    def default(self):
        def decorator(view):
            self.register(DefaultHandler, view)
            return view

        return decorator
