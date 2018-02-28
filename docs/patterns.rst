Bot patterns
============

When you create a new Bottery project, it will contain a file called `bot.py`.
This file is were you'll define what kind of messages your bot can receive and
what kind of responses it should return. 

First we need an instance of the Bottery main class. This is how we can access patterns of messages we are able to receive. We should define it such as:

.. code-block:: py

    from bottery import Bottery

    bot = Bottery()

Then all the patterns available in **bottery** will be available for use. You should define the pattern type you want as a decorator for a function. The function will be the return for that specific pattern when the pattern has a match. 

bot.patterns.message
^^^^^^^^^^^^^^^^^^^^

The pattern message allows your bot to check if a message was received. This way, **bottery** 
will check if that exact message was sent by the user. 
If the message was send exactly like you defined it, 
then the function is called to return a message. 

The default case is the one that comes when you first created your project:

.. code-block:: py

    @bot.patterns.message('ping')
    def pong(message):
        return 'pong'

You should remember that this pattern is not case-sensitive! If you wish to 
make a case-sensitive pattern, add a parameter on the decorator:

.. code-block:: py

    @bot.patterns.message('ping', case_sensitive=True)
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

You should remember that this pattern is not case-sensitive! If you wish to 
make a case-sensitive pattern, add a parameter on the decorator:

.. code-block:: py

    @bot.patterns.startswith('ping', case_sensitive=True)
    def pong(message):
        return 'pong'


bot.patterns.regex
^^^^^^^^^^^^^^^^^^

The *regex* pattern allows you to receive a message and will check for a regex pattern 
inside the message text. If there is a positive match, the view will be returned.

.. code-block:: py

    @bot.patterns.regex('\d+')
    def regex_answer(message):
        return 'It was a positive match'    

