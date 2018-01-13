from unittest import mock

import pytest

from bottery import handlers


@pytest.fixture
def test_handler():
    handler = type('TestHandler', (handlers.BaseHandler,), {})
    handler.clean_test = mock.MagicMock()

    def match(self, message):
        return True

    handler.match = match
    return handler()


def test_base_handler_full_clean(test_handler):
    test_handler.full_clean()
    assert test_handler.clean_test.called


def test_base_handler_check_calls_full_clean(test_handler):
    message = type('Message', (), {'text': 'ping'})
    test_handler.check(message)
    assert test_handler.clean_test.called


def test_message_handler_check():
    message = type('Message', (), {'text': 'ping'})
    handler = handlers.MessageHandler(pattern='ping')
    assert handler.check(message)


def test_message_handler_check_negative_match():
    message = type('Message', (), {'text': 'pong'})
    handler = handlers.MessageHandler(pattern='ping')
    assert not handler.check(message)


def test_message_handler_check_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = handlers.MessageHandler(pattern='Ping',
                                      case_sensitive=True)
    assert handler.check(message)


def test_message_handler_check_negative_match_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = handlers.MessageHandler(pattern='ping',
                                      case_sensitive=True)
    assert not handler.check(message)


def test_message_handler_check_negative_match_with_case_insensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = handlers.MessageHandler(pattern='ping',
                                      case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check():
    message = type('Message', (), {'text': 'hello my friend'})
    handler = handlers.StartswithHandler(pattern='hello')
    assert handler.check(message)


def test_startswith_handler_check_negative_match():
    message = type('Message', (), {'text': 'Ping'})
    handler = handlers.StartswithHandler(pattern='hello my friend')
    assert not handler.check(message)


def test_startswith_handler_check_with_case_sensitive():
    message = type('Message', (), {'text': 'Hello my friend'})
    handler = handlers.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check_negative_match_with_case_sensitive():
    message = type('Message', (), {'text': 'pong'})
    handler = handlers.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert not handler.check(message)


def test_default_handler_check():
    message = type('Message', (), {'text': 'pong'})
    assert handlers.DefaultHandler().check(message)


def test_regex_handler_check():
    message = type('Message', (), {'text': '20 pings'})
    handler = handlers.RegexHandler(pattern='\d+')
    assert handler.check(message)

def test_regex_handler_check_negative_match():
    message = type('Message', (), {'text': 'pings'})
    handler = handlers.RegexHandler(pattern='\d+')
    assert not handler.check(message)
