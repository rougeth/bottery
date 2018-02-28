.. _quickstart:

Quickstart
==========


Ping Pong Bot
---------------

Starting project
^^^^^^^^^^^^^^^^

Once Bottery is installed, you will be able to use the Bottery cli (command-line interface). To start a new project, run:

.. code-block:: bash

   $ bottery startproject librarybot

This will create a directory named ``librarybot`` in your current directory with the following files:

.. code-block:: bash

    librarybot/
        bot.py
        settings.py


* The outer ``librarybot/`` root directory is just a container for your project. It's name doesn't matter to Bottery, you can rename it to anything you like.
* ``librarybot/bot.py``: is where we define which messages we are able to receive and how to respond them;
* ``librarybot/settings.py``: Settings/configuration for the Bottery project.

Keep in mind that the name you'll choose for your project must be a valid identifier according to the language definition (`check the documentation for further information on identifiers <https://docs.python.org/3.6/reference/lexical_analysis.html#identifiers>`_).


Configuring token
^^^^^^^^^^^^^^^^^

For this example we'll use the Telegram Bot platform. The only thing you need to configure is the bot token on ``settings.py`` file. This token is generated when you create your bot on Telegram. For more info, check out how to create a new bot in the `Telegram documentation <https://core.telegram.org/bots#creating-a-new-bot>`_.

When you have the token, put it on the Telegram platform configurations:

.. code-block:: py

    PLATFORMS = {
        'telegram': {
            'ENGINE': 'bottery.platform.telegram',
            'OPTIONS': {
                'token': 'the-bot-token-here',
            }
        },
    }

Running
^^^^^^^

To run your bot just type:

.. code-block:: bash

    $ bottery run

That's it, there's nothing else to do. Your bot should be working now. Go to Telegram and type ``ping`` to your bot, it should respond with ``pong``.

Project Examples
^^^^^^^^^^^^^^^^

A small example of how bottery can work can be seen `here <https://github.com/leportella/bottery-examples>`_.
