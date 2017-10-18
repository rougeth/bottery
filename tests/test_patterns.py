from bottery.conf.patterns import (DefaultPattern, HookableFuncPattern,
                                   HookPattern, Pattern)


def test_pattern_instance():
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    assert pattern.pattern == 'ping'
    assert pattern.view == view


def test_pattern_check_right_message():
    '''
    Check if Pattern class return the view when message checks with
    pattern.
    '''
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'ping'})
    result = pattern.check(message)
    assert result == view


def test_pattern_check_wrong_message():
    '''
    Check if Pattern class returns False when message doesn't
    check with pattern.
    '''
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'pong'})
    assert not pattern.check(message)


def test_default_pattern_instance():
    def view(): return 'Hello world'
    pattern = DefaultPattern(view)
    assert pattern.view == view


def test_default_pattern_check_message():
    '''
    Check if DefaultPattern class return the message if any pattern
    is given.
    '''
    def view(): return 'Hello world'
    pattern = DefaultPattern(view)
    message = type('Message', (object,), {'text': 'ping'})
    result = pattern.check(message)
    assert result == view


def test_hook_pattern_no_hook():
    '''Check basic fields and False return if no hook
    active'''
    pattern = HookPattern('end')
    assert pattern._pattern is None
    assert pattern._end_hook_words == 'end'
    assert pattern.check(None) is False
    assert pattern.has_hook() is False


def test_hook_pattern_check_right_message():
    '''
    Check if Hook forwards to Pattern class
    return the view when message checks with
    pattern.
    '''
    '''
    Check if DefaultPattern class return the message if any pattern
    is given.
    '''
    def view(): return 'Hello world'
    pattern = DefaultPattern(view)
    message = type('Message', (object,), {'text': 'ping'})
    hook_pattern = HookPattern('end')
    hook_pattern.begin_hook(pattern)
    assert hook_pattern.has_hook() is True
    result = hook_pattern.check(message)
    assert result == view
    hook_pattern.end_hook()
    assert hook_pattern.has_hook() is False
    assert hook_pattern.check(message) is False


def test_hookable_func_pattern_instance():

    def view():
        return 'Hello world'

    def pre_process():
        return 'ping'

    hook_pattern = HookPattern()
    rules = {}
    params = {}
    pattern = HookableFuncPattern('ping', view, pre_process,
                                  hook_pattern, rules=rules, params=params)
    assert pattern.pattern == 'ping'
    assert pattern.view == view
    assert pattern.pre_process == pre_process
    assert pattern.context == []
    assert pattern.conversation == hook_pattern
    assert pattern.save_context is True
    assert pattern.rules == rules
    assert pattern.params == params


def test_hookable_func_pattern_right_message():

    def view():
        return 'Hello world'

    def pre_process(text):
        return text, 'params'

    hook_pattern = HookPattern()
    rules = {}
    params = {}
    pattern = HookableFuncPattern('ping', view, pre_process,
                                  hook_pattern, rules=rules, params=params)
    message = type('Message', (object,), {'text': 'ping'})
    assert pattern.check(message) is True


def test_hookable_func_pattern_wrong_message_and_hook():

    def view():
        return 'Hello world'

    def pre_process(text):
        return text, 'params'

    hook_pattern = HookPattern()
    rules = {}
    params = {}
    pattern = HookableFuncPattern('ping', view, pre_process,
                                  hook_pattern, rules=rules, params=params)
    message = type('Message', (object,), {'text': 'wrong'})
    assert pattern.check(message) is False
    # Now, activate Hook and test again
    hook_pattern.begin_hook(pattern)
    assert pattern.check(message) is True


def test_hookable_func_pattern_safe_call_view():

    def view(message):
        return message.text

    def pre_process(text):
        return text, 'params'

    hook_pattern = HookPattern()
    rules = {}
    params = {}
    pattern = HookableFuncPattern('ping', view, pre_process,
                                  hook_pattern, rules=rules, params=params)
    message = type('Message', (object,), {'text': 'one_value'})
    text, hook = pattern.safe_call_view(message)
    assert text == message.text
    assert hook is False


def test_hookable_func_pattern_call_view():
    '''HookableFuncPattern.callview Test'''

    def view(message):
        return view_result_list[ind]

    def pre_process(text):
        return text, 'params'

    view_result_list = [('one', True),
                        ('two', True),
                        ('end', False)]
    ind = 0
    hook_pattern = HookPattern()
    rules = {}
    params = {}
    pattern = HookableFuncPattern('ping', view, pre_process,
                                  hook_pattern, rules=rules, params=params)
    right_message = type('Message', (object,), {'text': 'ping'})
    wrong_message = type('Message', (object,), {'text': 'wrong'})
    assert pattern.check(wrong_message) is False
    assert pattern.check(right_message) is True
    # Call view that returns true must begin a Hook
    text = pattern.call_view(right_message)
    assert text == view_result_list[ind][0]
    assert hook_pattern.check(wrong_message) is True
    assert hook_pattern.check(right_message) is True
    # Repeating call must mantain the Hook
    ind = 1
    text = pattern.call_view(wrong_message)
    assert text == view_result_list[ind][0]
    assert hook_pattern.check(wrong_message) is True
    assert hook_pattern.check(right_message) is True
    # Last call (that returns false) must end the Hook
    ind = 2
    text = pattern.call_view(wrong_message)
    assert text == view_result_list[ind][0]
    assert hook_pattern.check(right_message) is False
