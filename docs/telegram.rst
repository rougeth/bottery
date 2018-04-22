Telegram
========

Widgets
-------

Reply
^^^^^

Telegram allows you to add a response as a reply to a particular message.
On *Bottery* you can define that a `view` will be returned as a reply to 
the last message by adding a decorator on the `view`:

.. code-block:: py

    from bottery.platform.telegram import reply 

    @reply()
    def hello(message):
        return 'Hello, there!' 

You can also send a parameter to the reply function so you can send reply messages 
to other messages that are not necessarily the last one.
To do so, add the decorator on the `view` and add a
function that will find the message id you want. For instance, if you want 
to reply not the last message, but the one before that you can do:

.. code-block:: py

    from bottery.platform.telegram import reply 

    @reply(lambda message: message.id - 1)
    def hello(message):
        return 'Hello, there!'
