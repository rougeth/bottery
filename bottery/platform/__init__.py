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

        return Response(source=message, text=response)

    def discovery_view(self, message):
        """
        Use the new message to search for a registered view according
        to its pattern.
        """
        for handler, view in self.registered_handlers:
            if handler.check(message):
                return view

        return None

    async def message_handler(self, data):
        """
        Process each new message:
        - Build specific platform message object
        - Find the responsible view
        - If any view was found, use it the process the response
        - If the view returned a string or a Response type, use it to
        send it to the user
        """

        message = self.build_message(data)
        if not message:
            logger.error(
                '[%s] Unable to build Message with data, data=%s, error',
                self.engine_name,
                data
            )
            return

        logger.info('[%s] New message from %s: %s', self.engine_name,
                    message.user, message.text)

        view = self.discovery_view(message)
        if not view:
            logger.info('[%s] View not found for %s message', self.engine_name,
                        message.id)
            return

        response = await self.get_response(view, message)
        if response:
            await self.send_response(response)
