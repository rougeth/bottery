Writing Views
=============

Defining a new response 
^^^^^^^^^^^^^^^^^^^^^^^

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


Working with templates
^^^^^^^^^^^^^^^^^^^^^^

Sometimes, you need complex and big messages to be returned by your patterns.
Bottery is able to render and respond messages using templates written in 
markdown. 

On your project directory, create a `template` folder. Your templates should be
kept inside this folder so Bottery can find them. For other configuration,
please check the `settings`  section. 

Let's create a template called `hello.md`:


.. code-block:: md

    Hello {{ user.first_name }}!

    Welcome to **Bottery**


Good! Now we need our view to respond with a template instead of a simple string.
To do this, we should user the method `render`:

.. code-block:: py
    
    from bottery.message import render

    def hello(message):
        return render(message, 'hello.md')


Bottery already gives you by default the message user on you template context.
If you need a new parameter on your template, just add a third parameter to 
the render function:

.. code-block:: py
    
    from bottery.message import render

    def hello(message):
        return render(message, 'hello.md', {'question': 'interested, yet?'})
