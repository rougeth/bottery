class BaseHandler:
    def __init__(self, pattern):
        self.pattern = pattern

    def check(self, message):
        raise NotImplementedError()


class BasicHandler(BaseHandler):
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

    def register(self, handler, view):
        self.registered.append((handler, view))

    def base(self, pattern):
        def decorator(handler):
            self.register(BasicHandler(pattern), handler)
            return handler

        return decorator

    def startswith(self, pattern):
        def decorator(handler):
            self.register(StartswithHandler(pattern), handler)
            return handler

        return decorator

    def default(self):
        def decorator(handler):
            self.register(DefaultHandler(), handler)
            return handler

        return decorator
