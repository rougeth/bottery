import logging

logger = logging.getLogger('bottery.messenger')


class MessengerAPI:
    url = 'https://graph.facebook.com/{0}{1}?access_token={2}'

    def __init__(self, token, session, version='v2.6'):
        self.token = token
        self.session = session
        self.version = version

    def make_url(self, method):
        return self.url.format(self.version, method, self.token)

    async def messages(self, user_id, text, type='RESPONSE'):
        request = {
            'messaging_type': type,
            'recipient': {
                'id': user_id,
            },
            'message': {
                'text': text,
            },
        }
        url = self.make_url('/me/messages')
        return await self.session.post(url, json=request)
