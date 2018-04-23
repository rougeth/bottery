Handlers patterns
=================

When you create a new Bottery project, it will contain a file called `handlers.py`. This file contains the rules that allow the bot to decide which view will respond the messages.

Here is a sample `handlers.py` file:

.. code-block:: py

    from bottery import handlers

    from views import pong

    msghandlers = [
        handlers.message('ping', pong)
    ]

If the bot receives a message that is exactly equal to `ping` the response will be the return value of the `pong` view function.

Bottery has the following handlers available:

``handlers.message``
--------------------

The message handler allows your bot to check if a message was received. This way, **bottery** will check if that exact message was sent by the user. If the message was send exactly like you defined it, then the view is used to return a message.

This is the handler that comes on `handlers.py` when you create a project:

.. code-block:: py

    msghandlers = [
        handlers.message('ping', pong)
    ]

You should remember that this pattern **is not case-sensitive**! If you wish to make a case-sensitive pattern, include the `case_sensitive` parameter:

.. code-block:: py

    msghandlers = [
        handlers.message('ping', pong, case_sensitive=True)
    ]


``handlers.startswith``
-----------------------

The *startswith* handler allows you to receive a message that only starts with a certain text, but not necessarily matches all message received.

.. code-block:: py

    def how_are_you(message):
        return 'Hello! How are you?'

    msghandlers = [
        handlers.startswith('hello', how_are_you)
    ]

With this pattern, if you receive a message such as `hello, my bot!` it will call our function and return an answer.

You should remember that this pattern **is not case-sensitive**! If you wish to make a case-sensitive pattern, include the `case_sensitive` parameter:

.. code-block:: py

    msghandlers = [
        handlers.startswith('hello', how_are_you, case_sensitive=True)
    ]


``handlers.regex``
------------------

The *regex* handler allows you to process a message that matches to a regex pattern. If there is a positive match, the view will be executed.

.. code-block:: py

    def numbers(message):
        return 'You sent only numbers!'

    msghandlers = [
        handlers.regex('\d+', numbers),
    ]

handlers.default
----------------

The *default* handler allows you to define view that will respond to any message. This should be used carefully, if the handler is defined above any other handler, those ones will never be reached.

.. code-block:: py

    def ops(message):
        return "Sorry, couldn't understand your message. Please, use /help to see the available options"

    msghandlers = [
        handlers.default(ops),
    ]

Process order
-------------

Note that **Bottery** will follow the order declared in `msghandlers` list to decide which handler will be used. It tries each handler pattern, in order, and stops at the first one that matches.

If you want to have a default handler, executed if no message is previously captured, you can use the following:

.. code-block:: py

    def default_response(message):
        return 'If nothing matches, this will be the response!'

    msghandlers = [
        # Include the handlers for the messages you want to reply
        (...)

        # This MUST be the last one and it will be executed if none of the
        # previously defined handlers matches the message
        handlers.default(default_response),
    ]
