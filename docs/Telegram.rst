Telegram
========

Add a reply response to last message
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Telegram allows you to add a response as a reply to a particular message.
On *Bottery* you can define that a `view` will be returned as a reply to 
the last message by adding a decorator on the `view`:

.. code-block:: py

    from bottery.platform.telegram import reply 

    @reply()
    def hello(message):
        return 'Hello, there!' 
