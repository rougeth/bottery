.. _installation:

Installation
============

Bottery depends on the awesome Python :py:mod:`asyncio` module and its :pep:`async and await<492>` syntax. So you will need to have Python 3.5 or newer installed to get started. If you need help to install Python on your computer, I strongly recommend the :ref:`Python Guide <pythonguide:installation>`.

tl;dr
-----

All right, nothing magic here, just use `pip` like you do to install any other Python package:

.. code-block:: bash

   $ pip install bottery

But if you are not using virtualenv, we strongly recommend you to continue reading the sections below.

Virtualenv
----------

Virtualenv is probably what you want to use during development, and if you have shell access to your production machines, you’ll probably want to use it there, too.

What problem does virtualenv solve? If you like Python as much as we do, chances are you want to use it for other projects besides Bottery-based web applications. But the more projects you have, the more likely it is that you will be working with different versions of Python itself, or at least different versions of Python libraries. Let’s face it: quite often libraries break backwards compatibility, and it’s unlikely that any serious application will have zero dependencies. So what do you do if two or more of your projects have conflicting dependencies?

Virtualenv to the rescue! Virtualenv enables multiple side-by-side installations of Python, one for each project. It doesn’t actually install separate copies of Python, but it does provide a clever way to keep different project environments isolated. Let’s see how virtualenv works.

Since Python 3.3, the :py:mod:`venv` is part of the Python buildin modules, which means that you won't need to install anything to work with virtualenvs.

Creation of :py:mod:`virtual environments <venv>` is done by executing the command venv:

.. code-block:: bash

   $ python3 -m venv /path/to/new/virtual/environment

Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s binary directory. The invocation of the script is platform-specific:

.. code-block:: bash

   $ source <venv>/bin/activate

For more details on how virtualenv works or how to use it on Windows, take a look at the :py:mod:`oficial documentation <venv>` and at the :pep:`405`.


System-Wide installation
------------------------

This is possible as well, though we do not recommend it. Just run pip with root privileges:

.. code-block:: bash

   $ sudo pip install bottery

Living on the Edge
------------------

Bottery is actively developed on GitHub, where the code is (and always will be) available under the MIT license.

You can either clone the public repository:

.. code-block:: bash

    $ git clone https://github.com/rougeth/bottery.git

Or, download the tarball:

.. code-block:: bash

    $ curl -OL https://github.com/rougeth/bottery/tarball/master
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily:

.. code-block:: bash

    $ cd bottery
    $ pip install .
