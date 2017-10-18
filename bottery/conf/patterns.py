'''Classes that do the comparison of the User words
 and a predefined pattern'''


class Pattern:
    '''Basic equal comparison'''

    def __init__(self, pattern, view):
        self.pattern = pattern
        self.view = view

    def check(self, message):
        if message.text == self.pattern:
            return self.view
        return False


class DefaultPattern:
    '''Check always True'''

    def __init__(self, view):
        self.view = view

    def check(self, message=None):
        # regarless the message, this pattern should return
        # the view, so, there is no checks to be made here
        return self.view


class FuncPattern(Pattern):
    '''Receives a function to preprocess the incoming message
    text before comparing it to the pattern.
    Allows use of regular expressions, selecting partial words for
    routing, etc'''

    def __init__(self, pattern, view, pre_process):
        self.pre_process = pre_process
        Pattern.__init__(self, pattern, view)

    def check(self, message):
        text, _ = self.pre_process(message.text)
        if text == self.pattern:
            return self.view
        return False


class HookableFuncPattern(Pattern):
    '''Receives a function to preprocess the incoming message
    text before comparing it to the pattern.
    Allows use of regular expressions, selecting partial words for
    routing, etc
    pre_process: a function to process message on check action before
     comparing with pattern
    context: string with history of messages
    conversation: HookPattern Object that will hook any next messages
     to this pattern (see ConversationPattern)'''

    def __init__(self, pattern, view, pre_process,
                 hook_pattern=None, save_context=True,
                 rules=None, params=None):
        self.pre_process = pre_process
        self.context = []
        self.conversation = hook_pattern
        self.save_context = save_context
        self.rules = rules
        self.params = params
        Pattern.__init__(self, pattern, view)

    def safe_call_view(self, message):
        '''Local function to check return of view.
        Just to treat errors if view returns only response'''
        from inspect import signature
        sig = signature(self.view)
        if str(sig).find('rules') == -1:
            tuple_return = self.view(message)
        else:
            tuple_return = self.view(message, self.rules, self.params)
        if isinstance(tuple_return, tuple):
            response = tuple_return[0]
            hook = tuple_return[1]
        else:
            response = tuple_return
            hook = False
        return response, hook

    def check(self, message):
        '''Simple check'''
        if (self.conversation is not None) and self.conversation.has_hook():
            return True
        text, _ = self.pre_process(message.text)
        if text == self.pattern:
            return True
        return False

    def call_view(self, message):
        ''' If a view wants to begin a conversation, it needs to return True
        Default is False.
        First we see if the context has to be set, then we run the view.
        While view returns True, the hook will remain'''
        # If hooked, go directly to view
        if (self.conversation is not None) and self.conversation.has_hook():
            if self.save_context:
                self.context.append(message.text)
                message.text = " ".join(self.context)
            response, hook = self.safe_call_view(message)
            if not hook:
                self.conversation.end_hook()
                self.context = []
            return response
        # Else, begin normal check
        text, _ = self.pre_process(message.text)
        if text == self.pattern:
            response, hook = self.safe_call_view(message)
            if hook:
                self.context = []
                self.context.append(text)
                if (self.conversation is not None) and  \
                        (not self.conversation.has_hook()):
                    self.conversation.begin_hook(self)
            return response
        return False


class HookPattern(Pattern):
    '''FirstPattern to be checked. Allows a Pattern to "capture" and release
    the flow if it receives an incomplete messsage
    _pattern: a Hookable Pattern Object
    end_hook_words: a list of words that terminates the Hook
    Usage:
    Put as first pattern. On a view, call set_conversation(Pattern)
     to ensure the next message will go to this Pattern
    Also on a view, call end_conversation to release the hook'''

    def __init__(self, end_hook_words=None):
        self._pattern = None
        self._end_hook_words = end_hook_words
        Pattern.__init__(self, "", None)

    def check(self, message):
        '''Pass the calling away'''
        if self._pattern is None:
            return False

        if self._end_hook_words is not None:
            for word in message.text.split(' '):
                if word in self._end_hook_words:
                    self.end_hook()
                    return False
        # print('Passing the calling!!!')
        return self._pattern.check(message)

    def begin_hook(self, apattern):
        '''Pass the pattern that will begin a conversation'''
        self._pattern = apattern

    def end_hook(self):
        '''Releases pointer to Pattern ending a conversation'''
        self._pattern = None

    def has_hook(self):
        '''Return if hook is active'''
        return self._pattern is not None

    def call_view(self, message):
        '''pass the calling away'''
        if self._pattern is None:
            return "Error: no pattern hooked"
        return self._pattern.call_view(message)
