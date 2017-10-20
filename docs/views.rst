Views
=====

When you receive a message on your bot, Bottery will try to find a view to process and respond that message. Here we are going to talk a little bit on how a view works and how you can create your own.

Creating a new view
^^^^^^^^^^^^^^^^^^^

A view on Bottery is nothing more than a function that receives a Message object and returns a string that contains the text (for now, only texts) to be used as response.

On the `patterns.py` file, you should define the messages you aim to receive and functions to return it. You can create a new function called `hello` that will return a string `Hello World`:


.. code-block:: py

    async def hello(message):
        return 'Hello world!'

Now, create a new pattern that receives the message `hello`, and returns our newly created view:


.. code-block:: py

    patterns = [
        Pattern('hello', hello)
    ]

Now your bot is able to respond a `hello` message.

Sync views
^^^^^^^^^^

In the Bottery documentation, all the views definitions uses the `async` keyword. That doesn't mean that every view on your bot must be defined with `asyncio` syntax. You just need to be careful when creating views as normal functions, since you can accidentally block your bot while executing this view by making a block operation, for example a request to an external API that takes too long.

Working with templates
^^^^^^^^^^^^^^^^^^^^^^

Sometimes, you need complex and big messages to be returned by your patterns.
Bottery is able to render and respond messages using templates written in
markdown.

On your project directory, create a folder named "**templates**". Your templates should be
kept inside this folder so Bottery can find them. For other configuration,
please check the `settings`  section.

Let's create a template called `hello.md`:

.. code-block:: md

    Hello {{ user.first_name }}!

    Welcome to **Bottery**

Good! Now we need our view to return a template instead of a simple string.
To do this, we should user the method `render`.

Render is a default function that can receive the following parameters:

*render(message, template_file, context={})*

Here is an example using render without needing any extra content:

.. code-block:: py

    from bottery.message import render

    async def hello(message):
        return render(message, 'hello.md')


Bottery already gives you by default the message user on you template context.
If you need a new parameter on your template, just add a third parameter to
the render function:

.. code-block:: py

    from bottery.message import render

    async def hello(message):
        return render(message, 'hello.md',
                      {'question': 'interested, yet?'})
