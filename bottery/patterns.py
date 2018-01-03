class BaseHandler:
    def __init__(self, pattern=None, *args, **kwargs):
        self.pattern = pattern
        self.kwargs = kwargs

    def check(self, message):
        self.message = self.message_filters(message)
        return self.match(self.message)

    def message_filters(self, message):
        return message

    def match(self, message):
        raise Exception('Method Not Implemented')


class CaseSensitiveMixinHandler:
    def message_filters(self, message):
        if not self.kwargs.get('case_sensitive'):
            message.text = message.text.lower()
        return message


class MessageHandler(BaseHandler, CaseSensitiveMixinHandler):
    def match(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithHandler(BaseHandler, CaseSensitiveMixinHandler):
    def match(self, message):
        if message.text.lower().startswith(self.pattern):
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
