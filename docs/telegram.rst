Telegram Widgets
================

``reply()``
-----------

.. function:: reply(to=None)

Telegram allows you to add a response as a reply to a particular message.
On *Bottery* you can define that a `view` will be returned as a reply to
the last message by adding a decorator on the `view`:

.. code-block:: py

    from bottery.telegram import reply

    @reply()
    def hello(message):
        return 'Hello, there!'

The argument `to` specificies a function of one argument of `Message` type that
is used to define which message should be replied. The expected return is an integer.

.. code-block:: py

    @reply(to=lambda message: message.id - 1)
    def hello(message):
        return 'Hello, there!'
