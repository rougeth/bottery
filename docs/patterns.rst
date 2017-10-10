Patterns
========

Pattern
^^^^^^^

Pattern is a class that will receive a pattern message and a view. If the 
message text is equal to the Pattern's pattern, it will return the view.

.. code-block:: py
   
    def hello(message):
        return 'Hello, world!' 

    patterns = [
        Pattern('hello', hello),
    ]


Default Pattern
^^^^^^^^^^^^^^^

Default Pattern is a class that will receive only a view. Regardless the
message it receives, it will always return the view. It can be used for a 
NotFound response, for instance.

As it will always return the view, you should add it on the patterns list as the
last element, otherwise it will always return the view and any other pattern listed
after it will be ignored.

.. code-block:: py
   
    from bottery.patterns import DefaultPattern

    def not_found(message):
        return "Sorry, I can't understand what you're saying :("

    patterns = [
        Pattern('hello', hello),
        DefaultPattern(not_found),
    ]
