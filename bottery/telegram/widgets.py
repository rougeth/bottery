import asyncio


class BaseDecorator:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def _add_request_payload(self, message):
        if message.platform == 'telegram':
            kwargs = self.prepare(message)
            message._request_payload.update(kwargs)

        return message

    def _call_async_wrapper(self, view):
        async def async_wrapper(message):
            message = self._add_request_payload(message)
            return await view(message)
        return async_wrapper

    def _call_sync_wrapper(self, view):
        def wrapper(message):
            message = self._add_request_payload(message)
            return view(message)
        return wrapper

    def __call__(self, view):
        if asyncio.iscoroutinefunction(view):
            return self._call_async_wrapper(view)

        return self._call_sync_wrapper(view)


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


class Reply(BaseDecorator):
    def prepare(self, message):
        reply_to = self.kwargs.get('to')
        if not reply_to:
            return {'reply_to_message_id': message.id}

        return {'reply_to_message_id': reply_to(message)}
