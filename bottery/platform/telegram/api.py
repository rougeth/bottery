def to_mixed_case(string):
    words = string.split('_')
    return words[0].lower() + ''.join([s.title() for s in words[1:]])


class TelegramAPI:
    api_url = 'https://api.telegram.org'
    methods = [
        'delete_webhook',
        'send_message',
        'set_webhook',
        'get_updates',
    ]

    def __init__(self, token, session):
        self.token = token
        self.session = session

    def make_url(self, method_name):
        method_name = to_mixed_case(method_name)
        return '{}/bot{}/{}'.format(self.api_url, self.token, method_name)

    def __getattr__(self, attr):
        if attr not in self.methods:
            raise AttributeError()

        url = self.make_url(attr)

        async def request(**kwargs):
            response = await self.session.post(url, json=kwargs)
            return await response.json()

        return request
