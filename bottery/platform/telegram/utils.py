import asyncio


class BaseDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, view):
        async def wrapper(message):
            if message.platform == 'telegram':
                kwargs = self.prepare(message)
                message._request_payload.update(kwargs)

            if asyncio.iscoroutinefunction(view):
                return await view(message)
            return view(message)

        return wrapper


class Keyboard(BaseDecorator):
    def prepare(self, message):
        resize_keyboard = getattr(self.kwargs, 'resize_keyboard', True)
        one_time_keyboard = getattr(self.kwargs, 'one_time_keyboard', True)

        reply_markup = {
            'keyboard': [],
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard,
        }

        for row in self.args[0]:
            buttons = []
            for button in row:
                buttons.append({'text': button})

            reply_markup['keyboard'].append(buttons)

        return {'reply_markup': reply_markup}
