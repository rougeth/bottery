.. _quickstart:

Quickstart
==========


Ping Pong Bot
---------------

In this first example, we will create a simple bot that respond ``pong`` when it receives ``ping``.


Starting project
^^^^^^^^^^^^^^^^

Once Bottery is installed, you will be able to use the Bottery cli (command-line interface). To start a new project, run:

.. code-block:: bash

   $ bottery startproject pingpongbot

This will create a directory named ``pingpongbot`` in your current directory with the following files:

.. code-block:: bash

    pingpongbot/
        views.py
        handlers.py
        settings.py
        wsgi.py


* The outer ``pingpongbot/`` root directory is just a container for your project. It's name doesn't matter to Bottery, you can rename it to anything you like.
* ``pingpongbot/views.py``: is where we define the functions that will respond to new messages;
* ``pingpongbot/handlers.py``: is where we tell Bottery what message patterns the views defined on ``views.py`` should respond to;
* ``pingpongbot/settings.py``: Settings/configuration for the Bottery project.
* ``pingpongbot/wsgi.py``: An entry-point for WSGI-compatible web servers to serve your project.

Keep in mind that the name you'll choose for your project must be a valid identifier according to the language definition (`check the documentation for further information on identifiers <https://docs.python.org/3.6/reference/lexical_analysis.html#identifiers>`_).


Configuring token
^^^^^^^^^^^^^^^^^

For this example we'll use the Telegram Bot platform. The only thing you need to configure is the bot token on ``settings.py`` file. This token is generated when you create your bot on Telegram. For more info, check out how to create a new bot in the `Telegram documentation <https://core.telegram.org/bots#creating-a-new-bot>`_.

When you have the token, put it on the Telegram platform configurations:

.. code-block:: py

    PLATFORMS = {
        'telegram': {
            'ENGINE': 'bottery.telegram',
            'OPTIONS': {
                'token': 'the-bot-token-here',
            }
        },
    }

Running
^^^^^^^

Before running your bot, remember that you need to be in the same folder of the ``settings.py`` file. Once in the same folder, just type:

.. code-block:: bash

    $ bottery run

That's it, there's nothing else to do. Your bot should be working now. Go to Telegram and type ``ping`` to your bot, it should respond with ``pong``. This happens because on ``views.py`` already have a view called ``ping`` that always returns ``pong``.

Project Examples
^^^^^^^^^^^^^^^^

A small example of how bottery can work can be seen `here <https://github.com/leportella/bottery-examples>`_.
