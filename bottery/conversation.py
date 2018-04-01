import logging

logger = logging.getLogger('bottery')


class Conversations:
    def __init__(self):
        self.conversations = {}

    def get_view(self, user_id):
        view = self.conversations.get(user_id)
        return view or False

    def register(self, response):
        view = getattr(response.source, '_response_handler')
        if not view:
            return

        user_id = response.source.user.id

        if user_id in self.conversations:
            logger.warning(('user_id (%s) already register on conversation. '
                            'It will be overwritten.'), user_id)

        self.conversations[user_id] = view

    def clear(self, user_id):
        if user_id in self.conversations:
            del self.conversations[user_id]
        else:
            logger.warning('user_id (%s) not registered in a conversation.',
                           user_id)

