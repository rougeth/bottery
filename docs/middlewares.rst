.. _middlewares:

Middlewares
===========

Middleware is a framework of hooks into Bottery’s message/response processing. It’s a light, low-level “plugin” system for globally altering Bottery’s input or output.


Writing your own middleware
---------------------------

A middleware factory is a callable that takes a get_response callable and returns a middleware. A middleware is a callable that takes a message and returns a response, just like a view.

A middleware can be written as a function that looks like this:

.. code-block:: python

    def simple_middleware(get_response):
        # One-time configuration and initialization.

        def middleware(message):
            # Code to be executed for each message before
            # the view (and later middleware) are called.

            response = get_response(message)

            # Code to be executed for each message/response after
            # the view is called.

            return response

        return middleware

Or it can be written as a class whose instances are callable, like this:

.. code-block:: python

    class SimpleMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
            # One-time configuration and initialization.

        def __call__(self, message):
            # Code to be executed for each message before
            # the view (and later middleware) are called.

            response = self.get_response(message)

            # Code to be executed for each message/response after
            # the view is called.

            return response

The **get_response** callable provided by Bottery might be the actual view (if this is the last listed middleware) or it might be the next middleware in the chain. The current middleware doesn’t need to know or care what exactly it is, just that it represents whatever comes next.


Activating middlware
--------------------

To activate a middleware component, add it to the **MIDDLEWARES** list in your Django settings.

.. code-block:: python

    MIDDLEWARES = [
        SimpleMiddleware,
    ]

