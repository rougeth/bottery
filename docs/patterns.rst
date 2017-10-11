Patterns
========

When you create a new Bottery project, it will contain a file called `patterns.py`.
This file is were you will define what kind of messages your bot can receive and
what kind of responses you should return. Just remeber that Bottery will check the patterns list 
in order, so any generic message should be listed last, while more specific messages should have
the patterns listed first.

On your `pattern.py` file you should have a list named **patterns** containing different
kind of pattern classes. By default, Bottery will import the `Pattern` class, which is the most
simple type of pattern you can have: it should have a message that will "trigger" this pattern
and a function that will tell Bottery what it should return. However, our plan is that 
Bottery should allow you to have different kind of pattern classes that will allow you to have 
regex, natural language processing tools, among others. 

Pattern
^^^^^^^

*Pattern(pattern, view)* 

Pattern is a pattern class that will receive a pattern message and a view. If the 
message text is equal to the Pattern's pattern, it will return the view.

Here is an example of how you use a Pattern class on your `patterns.py`:

.. code-block:: py
   
    def hello(message):
        return 'Hello, world!' 

    patterns = [
        Pattern('hello', hello),
    ]


Default Pattern
^^^^^^^^^^^^^^^

*DefaultPattern(view)* 

DefaultPattern is a pattern class that will only receive a view. Regardless the
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
