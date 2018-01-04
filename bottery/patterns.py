class BaseHandler:
    def __init__(self, pattern=None, *args, **kwargs):
        self.pattern = pattern
        self.kwargs = kwargs

    def check(self, message):
        self.message = message
        self.full_clean()
        return self.match(self.message)

    def full_clean(self):
        for method_name in dir(self):
            if method_name.startswith('clean_'):
                method = getattr(self, method_name)
                method()

    def match(self, message):
        raise Exception('Method Not Implemented')


class CaseSensitiveMixinHandler:
    def clean_case_senstive(self):
        if not self.kwargs.get('case_sensitive'):
            self.message.text = self.message.text.lower()


class MessageHandler(CaseSensitiveMixinHandler, BaseHandler):
    def match(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithHandler(CaseSensitiveMixinHandler, BaseHandler):
    def match(self, message):
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
