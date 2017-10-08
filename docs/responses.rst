Responses
=========

Defining new responses 
^^^^^^^^^^^^^^^^^^^^^^

On the patterns file, you should define the messages you aim to receive and
functions to return it. By default, there is a `ping` function, there will
return a string `pong`. Define a new function called `hello`:

.. code-block:: py

    def hello(message):
        return 'Hello world!'

Now, create a new pattern that receives a message, and returns our newly
created function:


.. code-block:: py

    patterns = [
        Pattern('hello', hello)
    ]

Now your bot is able to return a message when receiving a 'hello'.
