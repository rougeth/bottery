import inspect
import logging

from bottery.message import Response


logger = logging.getLogger('bottery.platforms')


class BaseEngine:
    # Should we use ABC for required attributes and methods?

    def __init__(self, **kwargs):
        self.tasks = []

        kwargs['engine_name'] = kwargs.get('engine_name', '')
        # For each named parameters received, set it as an instance
        # attribute
        for item, value in kwargs.items():
            setattr(self, item, value)

    @property
    def platform(self):
        """Platform name"""
        raise NotImplementedError('platform attribute not implemented')

    def build_message(self):
        """
        Build Message instance according to the data received from the
        platform API.
        """
        raise NotImplementedError('build_message not implemented')

    async def configure(self):
        """Called by App instance to configure the platform"""
        raise NotImplementedError('configure not implemented')

    async def get_response(self, view, message):
        """
        Get response running the view with await syntax if it is a
        coroutine function, otherwise just run it the normal way.
        """

        if inspect.iscoroutinefunction(view):
            response = await view(message)
        else:
            response = view(message)

        if isinstance(response, Response):
            return response

        response = Response(source=message, text=response)
        self._activate_conversation(response)

        return response

    def _activate_conversation(self, response):
        self.conversations.register(response)

    def _check_conversations(self, message):
        user_id = message.user.id
        return self.conversations.get_view(user_id)

    def _clear_conversation(self, message):
        user_id = message.user.id
        self.conversations.clear(user_id)

    def discovery_view(self, message):
        """
        Check if user already has a conversation going on, if not,
        use the new message to search for a registered view according
        to its pattern.
        """
        view = self._check_conversations(message)
        if view:
            self._clear_conversation(message)
            return view

        for handler, view in self.registered_handlers:
            if handler.check(message):
                return view

        return None
