class BaseDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, view):
        def wrapper(message):
            if message.platform == 'telegram':
                kwargs = self.prepare(message)
                message._request_payload.update(kwargs)

            return view(message)

        return wrapper


class Keyboard(BaseDecorator):
    def prepare(self, message):
        reply_markup = {
            'keyboard': [],
            'resize_keyboard': self.kwargs.get('resize_keyboard', True),
            'one_time_keyboard': self.kwargs.get('one_time_keyboard', True),
        }

        for row in self.args[0]:
            buttons = []
            for button in row:
                buttons.append({'text': button})

            reply_markup['keyboard'].append(buttons)

        return {'reply_markup': reply_markup}
