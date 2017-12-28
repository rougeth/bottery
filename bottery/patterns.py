class BaseHandler:
    def __init__(self, pattern=None, sensitive=True):
        self.pattern = pattern
        self.sensitive = sensitive

    def check(self, message):
        raise Exception('check method not implemented')


class MessageHandler(BaseHandler):
    def check(self, message):
        filters = [
            message.text == self.pattern,
            not self.sensitive and message.text.lower() == self.pattern,
        ]

        if any(filters):
            return True
        return False


class StartswithHandler(BaseHandler):
    def check(self, message):
        filters = [
            message.text.startswith(self.pattern),
            not self.sensitive and \
              message.text.lower().startswith(self.pattern),
        ]

        if any(filters):
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

    def message(self, pattern, sensitive=True):
        def decorator(view):
            self.register(MessageHandler, view, pattern, sensitive)
            return view

        return decorator

    def startswith(self, pattern, sensitive=True):
        def decorator(view):
            self.register(StartswithHandler, view, pattern, sensitive)
            return view

        return decorator

    def default(self):
        def decorator(view):
            self.register(DefaultHandler, view)
            return view

        return decorator
