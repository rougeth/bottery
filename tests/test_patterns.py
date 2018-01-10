from unittest import mock

import pytest

from bottery import patterns


@pytest.fixture
def test_handler():
    handler = type('TestHandler', (patterns.BaseHandler,), {})
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
    handler = patterns.MessageHandler(pattern='ping')
    assert handler.check(message)


def test_message_handler_check_negative_match():
    message = type('Message', (), {'text': 'pong'})
    handler = patterns.MessageHandler(pattern='ping')
    assert not handler.check(message)


def test_message_handler_check_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.MessageHandler(pattern='Ping',
                                      case_sensitive=True)
    assert handler.check(message)


def test_message_handler_check_negative_match_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.MessageHandler(pattern='ping',
                                      case_sensitive=True)
    assert not handler.check(message)


def test_message_handler_check_negative_match_with_case_insensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.MessageHandler(pattern='ping',
                                      case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check():
    message = type('Message', (), {'text': 'hello my friend'})
    handler = patterns.StartswithHandler(pattern='hello')
    assert handler.check(message)


def test_startswith_handler_check_negative_match():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.StartswithHandler(pattern='hello my friend')
    assert not handler.check(message)


def test_startswith_handler_check_with_case_sensitive():
    message = type('Message', (), {'text': 'Hello my friend'})
    handler = patterns.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check_negative_match_with_case_sensitive():
    message = type('Message', (), {'text': 'pong'})
    handler = patterns.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert not handler.check(message)


def test_default_handler_check():
    message = type('Message', (), {'text': 'pong'})
    assert patterns.DefaultHandler().check(message)


def test_patterns_handlers():
    handler = patterns.PatternsHandler()
    assert not handler.registered


def test_patterns_handler_message():
    handler = patterns.PatternsHandler()
    decorator = handler.message('ping')

    def view():
        pass

    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered


def test_patterns_handler_startswith():
    handler = patterns.PatternsHandler()
    decorator = handler.startswith('ping')

    def view():
        pass

    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered
