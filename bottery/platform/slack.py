import asyncio
import logging

from slackclient import SlackClient

from bottery import platform
from bottery.message import Message
from bottery.platform import discover_view
from bottery.user import User

logger = logging.getLogger('bottery.slack')


class SlackUser(User):
    def __init__(self, sender):
        self.id = sender
        self.first_name = None
        self.last_name = None
        self.username = None
        self.language = None

    def __str__(self):
        return self.id


class SlackEngine(platform.BaseEngine):
    platform = 'slack'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = SlackClient(self.token)

        # If no `mode` was defined at settings.py, use by default
        # websocket mode.
        if not hasattr(self, 'mode'):
            self.mode = 'websocket'

    @property
    def tasks(self):
        return [self.websocket]

    def configure(self):
        self.client.rtm_connect()

    async def websocket(self, *args, **kwargs):
        # Handle each new message, send its responses and then request
        # updates again. Currently, the `rtm_read` method only receives a
        # single frame, so we exhaust the buffer before handling messages.
        messages = []
        while True:
            message = self.client.rtm_read()
            if message and message[0].get('type') == 'message':
                messages.extend(message)
            if not message:
                break
        tasks = [self.message_handler(msg) for msg in messages]
        await asyncio.gather(*tasks)
        asyncio.ensure_future(self.websocket())

    def build_message(self, data):
        """
        Return a Message instance according to the data received from
        Slack RTM API.
        """
        return Message(
            id=None,
            platform=self.platform,
            text=data['text'],
            user=SlackUser(data['user']),
            timestamp=data['ts'],
            raw=data,
        )

    async def message_handler(self, data):
        """
        Pass message to views
        """
        message = self.build_message(data)

        # Try to find a view (best name?) to respond to the message
        view = discover_view(message)
        if not view:
            return

        response = view(message)

        data = {
            'channel': data['channel'],
            'message': response,
        }
        # TODO: Verify response status
        self.client.rtm_send_message(data['channel'], data['message'])
        await asyncio.sleep(0)


engine = SlackEngine
