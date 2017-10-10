.. _quickstart:

Quickstart
==========


PingPong Bot
---------------

Starting project
^^^^^^^^^^^^^^^^

Once Bottery is installed, you will be able to use the Bottery cli (command-line interface). For starting a new project, run:

.. code-block:: bash

   $ bottery startproject librarybot

This will create a directory named `librarybot` in your current directory with files inside:

.. code-block:: bash

    librarybot/
        patterns.py
        settings.py


* The outer *librarybot/* root directory is just a container for your project. Its name doesn’t matter to Bottery, you can rename it to anything you like.
* *librarybot/patterns.py*: The Pattern declarations for this Bottery project;
* *librarybot/settings.py*: Settings/configuration for this Bottery project.


Configuring token
^^^^^^^^^^^^^^^^^

For this example we will use Telegram Bot platform. The only thing you need to configure is the bot token on `setting.py` file. This token is generated when you create your bot on Telegram. For more info, see Telegram documentation.

When you have the token, put it on Telegram platform configurations:

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

That's it, there's nothing else to do. Your bot should be working know. Go to Telegram and type `ping` to your bot, it should respond with `pong`.

Project Examples
^^^^^^^^^^^^^^^^

A small example of how bottery can work can be seen [here](https://github.com/leportella/bottery-examples)
