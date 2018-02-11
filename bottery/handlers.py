import re


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


class RegexHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = None

    def match(self, message):
        if not self.regex:
            self.regex = re.compile(self.pattern)

        if self.regex.match(message.text):
            return True
        return False


class CaseSensitiveMixin:
    def clean_case_senstive(self):
        if not self.kwargs.get('case_sensitive'):
            self.message.text = self.message.text.lower()


class MessageHandler(CaseSensitiveMixin, BaseHandler):
    def match(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithHandler(CaseSensitiveMixin, BaseHandler):
    def match(self, message):
        if message.text.startswith(self.pattern):
            return True
        return False


class DefaultHandler:
    def check(self, message):
        return True
