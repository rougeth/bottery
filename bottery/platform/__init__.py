import inspect
import logging

from bottery.message import Response
from bottery.conf import settings


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

    async def _get_response(self, message):
        """
        Get response running the view with await syntax if it is a
        coroutine function, otherwise just run it the normal way.
        """

        view = self.discovery_view(message)
        if not view:
            logger.info('[%s] View not found for %s message',
                        self.engine_name, message.id)
            return

        if inspect.iscoroutinefunction(view):
            response = await view(message)
        else:
            response = view(message)

        if isinstance(response, Response):
            return response

        return Response(source=message, text=response)

    async def prepare_get_response(self):
        get_response = self._get_response
        for middleware in reversed(settings.MIDDLEWARES):
            get_response = await middleware(get_response)

        return get_response

    async def get_response(self, message):
        f = await self.prepare_get_response()
        return await f(message)

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
        For each new message, build its platform specific message
        object and get a response.
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

        response = await self.get_response(message)
        if response:
            await self.send_response(response)
