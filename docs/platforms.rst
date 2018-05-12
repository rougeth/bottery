.. _platforms:

Platforms
=========

Bottery has a simples way to integrate to a chat plaform, and it's design is made in a such a way that it could, eventually, integrate to any chat platform. For now, Bottery works with two chat platforms , Facebook Messenger and Telegram but it give the tools to easly integrate to any other chat platform.

All of this platforms has different needs and different settings, but the views, when written without using specific platform features, should work for all of them.

Operation Modes
---------------

The first part of Bottery operation is when and how it gets new messages. Bottery receive messages in two different ways: polling and webhook;

Webhook
^^^^^^^

For every new message or event (eg. user read/edit/exlude a message), a HTTP request will be sent to a webserver provided by Bottery. Once Bottery gets this request, it will process each message and respond the ones that needs to be responded.

This is the most used approach by chatbot platforms. It's also the most complicated one to develop because it needs to have the bot running over the internet, so that those requests made by the platform can actually gets to Bottery.

An option to develop the bot on platforms that uses webhook option is to create tunnels to the bot running locally. `ngrok <https://ngrok.com>`_ is an option that creates a secure tunnel and expose a local `ip:port` to the internet.

Remember to always have `HOSTNAME` and `SECRET_KEY` configured on `settings.py`:

.. code-block:: py

   # settings.py
   HOSTNAME = 'example.com'


Polling
^^^^^^^

The polling option consist in checking from time to time if the platform has new messages. Bottery keeps constantly making requests to the platform API asking for new messages.

For production, use `Webhook`_ mode so that the bot receives new messages when they are actually sent.


Telegram
--------

When you create a new Bottery project, the `settings.py` file comes with everything needed to create a Telegram chatbot. This is because Telegram is the most open chatbot platform available. They have lots of features, like buttons, different keyboards, audio and video messages, location share, groups and even in-app payments. There is also no bureaucracy to have your chatbot exchange messages with real users.

The first step is to create the bot at Telegram by following the instructions at the `official documentation <https://core.telegram.org/bots>`__ and once it's done, Telegram will give a token to be used on Bottery. The `token` is required to authorize the bot and send requests to the Telegram Bot API.

Besides the `token`, the `mode` the bot will operates can be configured at `settings.py`, like the example below (if no one is configured, `polling` will be used):

.. code-block:: py

   # settings.py
   PLATFORMS = {
        'telegram': {
            'ENGINE': 'bottery.telegram',
            'OPTIONS': {
                'token': 'your-bot-token',
                'mode': 'polling',  # or 'webhook'
            }
        }
        # ...
   }

Facebook Messenger
------------------

The Messenger platform is more restricted. `webhook` mode is the only option available and before your bot gets to production, it's needed to be submitted for `revision <https://developers.facebook.com/docs/messenger-platform/submission-process>`_. Just like `Telegram`_, you need to set the `token` option at `settings.py`. See the `official documentation <https://developers.facebook.com/docs/messenger-platform>`__ for creating and getting the `token` for the bot. Since Messenger doesn't support `polling` mode, it needs to have `HOSTNAME` and `SECRET_KEY` configured at `settings.py`:

.. code-block:: py

   # settings.py
   HOSTNAME = 'example.org',
   SECRET_KEY = 'super-secret-key',

   PLATFORMS = {
        'messenger': {
            'ENGINE': 'bottery.messenger',
            'OPTIONS': {
                'token': 'your-bot-token',
            }
        }
        # ...
   }
