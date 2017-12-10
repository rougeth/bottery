class BasePattern:
    def __init__(self, pattern):
        self.pattern = pattern

    def check(self, message):
        raise ImproperlyConfiguredError()


class BasicPattern(BasePattern):
    def check(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithPattern(BasePattern):
    def check(self, message):
        if message.text.startswith(self.pattern):
            return True
        return False


class DefaultPattern:
    def check(self, message):
        return True


class PatternsHandler:
    def __init__(self):
        self.registered = []

    def exactly(self, pattern):
        def decorator(handler):
            self.registered.append((BasicPattern(pattern), handler))
            return handler

        return decorator

    def startswith(self, pattern):
        def decorator(handler):
            self.registered.append((StartswithPattern(pattern), handler))
            return handler

        return decorator

    def default(self, pattern):
        def decorator(handler):
            self.registered.append((DefaultPattern(Pattern), handler))
            return handler

        return decorator