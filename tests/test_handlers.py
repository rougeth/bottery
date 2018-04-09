from unittest import mock

import pytest

from bottery import handlers


@pytest.fixture
def message():
    return type('Message', (), {'text': 'ping'})


@pytest.fixture
def handler():
    handler = type('TestHandler', (handlers.BaseHandler,), {})
    handler.clean_test = mock.MagicMock()

    def match(self, message):
        return True

    handler.match = match
    return handler()


def test_base_handler_full_clean(handler):
    handler.full_clean()
    assert handler.clean_test.called


def test_base_handler_check_calls_full_clean(handler, message):
    handler.check(message)
    assert handler.clean_test.called


def test_message_handler_check(message):
    handler = handlers.MessageHandler(pattern='ping')
    assert handler.check(message)


def test_message_handler_check_negative_match(message):
    message.text = 'pong'
    handler = handlers.MessageHandler(pattern='ping')
    assert not handler.check(message)


def test_message_handler_check_with_case_sensitive(message):
    message.text = 'Ping'
    handler = handlers.MessageHandler(pattern='Ping',
                                      case_sensitive=True)
    assert handler.check(message)


def test_message_handler_check_negative_match_with_case_sensitive(message):
    message.text = 'Ping'
    handler = handlers.MessageHandler(pattern='ping',
                                      case_sensitive=True)
    assert not handler.check(message)


def test_message_handler_check_negative_match_with_case_insensitive(message):
    message.text = 'Ping'
    handler = handlers.MessageHandler(pattern='ping',
                                      case_sensitive=False)
    assert handler.check(message)


def test_platform_option_match(message):
    message.platform = 'telegram'
    handler = handlers.MessageHandler(pattern='ping',
                                      platforms=['telegram'])
    assert handler.check(message)


def test_platform_option_not_match(message):
    message.platform = 'telegram'
    handler = handlers.MessageHandler(pattern='ping',
                                      platforms=['messenger'])
    assert not handler.check(message)


def test_startswith_handler_check(message):
    message.text = 'hello my friend'
    handler = handlers.StartswithHandler(pattern='hello')
    assert handler.check(message)


def test_startswith_handler_check_negative_match(message):
    message.text = 'Ping'
    handler = handlers.StartswithHandler(pattern='hello my friend')
    assert not handler.check(message)


def test_startswith_handler_check_with_case_sensitive(message):
    message.text = 'hello my friend'
    handler = handlers.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check_negative_match_with_case_sensitive(message):
    message.text = 'pong'
    handler = handlers.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert not handler.check(message)


def test_default_handler_check(message):
    message.text = 'pong'
    assert handlers.DefaultHandler().check(message)


def test_regex_handler_check(message):
    message.text = '20 pings'
    handler = handlers.RegexHandler(pattern='\d+')
    assert handler.check(message)


def test_regex_handler_check_negative_match(message):
    message.text = 'pings'
    handler = handlers.RegexHandler(pattern='\d+')
    assert not handler.check(message)


@mock.patch('re.compile')
def test_regex_handler_double_match(mocked_compile, message):
    handler = handlers.RegexHandler(pattern='\d+')
    message.text = 'pings'

    handler.match(message)
    handler.match(message)
    assert handler.regex
    assert mocked_compile.call_count == 1
