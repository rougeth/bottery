Bot patterns
========

When you create a new Bottery project, it will contain a file called `bot.py`.
This file is were you will define what kind of messages your bot can receive and
what kind of responses you should return. 

First we need to an instance of the Bottery main class. This is how we can access patterns of messages we are able to receive. We should define it such as:

.. code-block:: py

    from bottery import Bottery

    bot = Bottery()

Then all the patterns available in **bottery** will be available for use. You should define the pattern type you wante was a decorator for a function. The function will be the return for that specific pattern when the pattern has a match. 

bot.patterns.message
^^^^^^^^^^^^^^^^^^^^

The pattern message allows your bot to check if a message was received. This way, **bottery** 
will check if that exact message was sent by the user. 
If the message was send exactly like you defined it, then the function is called to return a message. 

You should remember that this pattern is case-sensitive!

The default case is the one that comes when you first created your project:

.. code-block:: py

    @bot.patterns.message('ping')
    def pong(message):
        return 'pong'

bot.patterns.startswith
^^^^^^^^^^^^^^^^^^^^^^^

The *startswith* pattern allows you to receive a message that only starts with a certain text, 
but not necessarily matches all message received. 

.. code-block:: py

    @bot.patterns.startwith('hello')
    def how_are_you(message):
        return 'Hello! How are you?'

With this pattern, if you receive a message such as `hello, my bot!` it will call our function and 
return an answer.

