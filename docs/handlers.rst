Handlers patterns
=================

When you create a new Bottery project, it will contain a file called `handlers.py`.
This file contains the rules that allow the bot to decide the response to a message,
based on its content.

Here is a sample `handlers.py` file:

.. code-block:: py

    from bottery import handlers

    from views import pong

    msghandlers = [
        handlers.message('ping', pong)
    ]

If the bot receives a message is exactly equal to `ping` the response will be the return value
of the `pong` function.

Bottery has the following handlers available:

handlers.message
----------------

The message handler allows your bot to check if a message was received. This way, **bottery**
will check if that exact message was sent by the user. If the message was send exactly like
you defined it, then the function is called to return a message.

The default case is the one that comes when you first created your project:

.. code-block:: py

    msghandlers = [
        handlers.message('ping', pong)
    ]

You should remember that this pattern **is not case-sensitive**! If you wish to
make a case-sensitive pattern, include the `case_sensitive` parameter:

.. code-block:: py

    msghandlers = [
        handlers.message('ping', pong, case_sensitive=True)
    ]


handlers.startswith
-------------------

The *startswith* handler allows you to receive a message that only starts with a certain text,
but not necessarily matches all message received.

.. code-block:: py

    def how_are_you(message):
        return 'Hello! How are you?'

    msghandlers = [
        handlers.startswith('hello', how_are_you)
    ]

With this pattern, if you receive a message such as `hello, my bot!` it will call our function and
return an answer.

You should remember that this pattern **is not case-sensitive**! If you wish to
make a case-sensitive pattern, include the `case_sensitive` parameter:

.. code-block:: py

    msghandlers = [
        handlers.startswith('hello', how_are_you, case_sensitive=True)
    ]


handlers.regex
--------------

The *regex* handler allows you to process a message that matches to a regex pattern.
If there is a positive match, the view will be executed.

.. code-block:: py

    def numbers(message):
        return 'You sent only numbers!'

    msghandlers = [
        handlers.regex('\d+', numbers),
    ]

Processing order
----------------

Note that Bottery will try to match the message content to the handlers following the order
declared in `msghandlers` list and when it found one

Bottery runs through each handler pattern, in order, and stops at the first one that matches.

If you want to have a default handler, executed if no message is previously captured, you can use
the following:

.. code-block:: py

    def default_response(message):
        return 'If nothing matches, this will be the response!'

    msghandlers = [
        # Include the handlers for the messages you want to reply
        (...)

        # This MUST be the last one and it will be executed if none of the
        # previously defined handlers matches the message
        handlers.regex('.*', default_response),
    ]