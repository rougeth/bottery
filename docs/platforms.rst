.. _platforms:

Platforms
=========

Bottery design always considered the possibility to integrate to any chat platform. At the code level, there're many abstractions to make it possible. Bottery works out of the box with two chat platforms, Facebook Messenger and Telegram but it give the tools to easly integrate to any specific platform.

All of this platforms has different needs and different settings, but the views, when written without using specific platform features, should work for all of them.

Operation Modes
---------------

The first part of Bottery operation is when it get new messages. And Bottery do it throut two different ways: polling and webhook;

Webhook
^^^^^^^

For every new message or event (eg. user read/edit/exlude a message), a HTTP request will be sent to a webserver provided by Bottery. Once Bottery get this request, it will process each message and respond the ones that needs to be responded.

This is the approach most used by chatbot platforms and also the most complicated one.

Remember to configure `HOSTNAME` and `SECRET_KEY` on your `settings.py`, there to settings will be used to configure the webhook on the platform:

.. code-block:: py

   # settings.py
   HOSTNAME = 'example.com'
   SECRET_KEY = 'super-secret-key'

An option to develop your bot on platforms that uses webhook option is to create tunnels to the Bottery running locally. `ngrok`_ is an option that creates a secure tunnel and expose Bottery running locally to the internet.

.. _ngrok: https://ngrok.com/


Polling
^^^^^^^

The polling option consist in checking from time to time if the platform has new messages. Bottery keeps constantly making requests to the platform API asking for new messages.


Telegram
--------

When you create a new Bottery project, the `settings.py` file comes with everything needed to create a Telegram chatbot. This is because Telegram is the most open chatbot platform available. They have a lot of features, like buttons and different keyboards, audio and video messages, location share, group and even in-app payments. There is also no bureaucracy to have your chatbot exchange messages with real users.

Facebook Messenger
------------------

Create your integration
-----------------------

