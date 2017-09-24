import os
import tempfile
from datetime import datetime
from unittest import mock

from bottery.message import Message, render


def test_message_instance():
    message = Message(123, 'Telegram', 'Bottery', 'text', 1506191745, 'raw')
    assert message.datetime.year == 2017
    assert message.datetime.month == 9
    assert message.datetime.day == 23


@mock.patch('bottery.message.settings')
def test_render(mocked_settings):
    '''
    Test if a message template is rendered with a
    specified context.
    '''
    message = Message(123, 'Telegram', 'Bottery', 'text', 1506191745, 'raw')
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, 'templates')
        os.mkdir(path)

        template_path = os.path.join(path, 'template.md')
        with open(template_path, 'w') as template:
            template.write('{{ user }} {{ text }}!')

        mocked_settings.TEMPLATES = [path]
        rendered = render(message, 'template.md', {'text': 'rocks'})
        assert rendered == 'Bottery rocks!'
