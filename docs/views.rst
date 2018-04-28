Views
=====

A view function is simply a Python function that takes a message, process it and
returns or not a response. If the view returns a `str` or a **Response**
object, Bottery will use the returned object as a response. If it doesn't
returns anything, Bottery will consider that message doesn't need response.


Working with templates
^^^^^^^^^^^^^^^^^^^^^^

Sometimes you need complex and big messages to be returned by your patterns.
Bottery is able to render and respond messages using templates written in
markdown.

On your project directory, create a folder named "**templates**". Your templates
should be kept inside this folder so Bottery can find them. For other configuration,
please check the `settings`  section.

Let's create a template called `hello.md`:

.. code-block:: md

    Hello {{ user.first_name }}!

    Welcome to **Bottery**

Good! Now we need our view to return a template instead of a simple string.
To do this, we should use the method `render`.

Render is a default function that can receive the following parameters:

*render(message, template_file, context={})*

Here is an example using render without needing any extra content:

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
        return render(message, 'hello.md',
                      {'question': 'interested, yet?'})
