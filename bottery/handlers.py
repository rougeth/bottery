import re
from functools import partial

from bottery.exceptions import ValidationError


class CaseSensitiveOptionMixin:
    def clean_case_senstive(self):
        if not self.kwargs.get('case_sensitive'):
            self.message.text = self.message.text.lower()


class PlatformsOptionMixin:
    def clean_platforms(self):
        platforms = self.kwargs.get('platforms')

        if platforms is None:
            return

        if not isinstance(platforms, (list, tuple,)):
            raise Exception('platforms option must be a list or a tuple')

        if self.message.platform not in platforms:
            raise ValidationError('message not from {}'.format(platforms))


class BaseHandler(PlatformsOptionMixin):
    def __init__(self, pattern=None, *args, **kwargs):
        self.pattern = pattern
        self.kwargs = kwargs

    def check(self, message):
        self.message = message
        try:
            self.full_clean()
        except ValidationError:
            return False
        else:
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


class MessageHandler(CaseSensitiveOptionMixin, BaseHandler):
    def match(self, message):
        if message.text == self.pattern:
            return True
        return False


class StartswithHandler(CaseSensitiveOptionMixin, BaseHandler):
    def match(self, message):
        if message.text.startswith(self.pattern):
            return True
        return False


class DefaultHandler(BaseHandler):
    def check(self, message):
        return True


def _handle_msg(pattern, view=None, Handler=None, *args, **kwargs):
    if not view:
        # Hello, I'm a hack! Nice to meet up
        view, pattern = pattern, view

    return (Handler(pattern, **kwargs), view)


default = partial(_handle_msg, Handler=DefaultHandler)
message = partial(_handle_msg, Handler=MessageHandler)
regex = partial(_handle_msg, Handler=RegexHandler)
startswith = partial(_handle_msg, Handler=StartswithHandler)
