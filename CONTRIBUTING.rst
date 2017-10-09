Contributing
============

Contributions are highly welcomed and appreciated.  Every little help counts,
so do not hesitate!

Contributions can be made in the form of feature requests, bug reports and feedback.


First Time
----------

- Download and install the `latest version of git`_.
- Configure git with your `username`_ and `email`_::

    $ git config --global user.name 'your name'
    $ git config --global user.email 'your email'

- Make sure you have a `GitHub account`_.
- Fork Bottery to your GitHub account by clicking the `Fork`_ button.
- `Clone`_ your GitHub fork locally::

    $ git clone https://github.com/{username}/bottery/
    $ cd bottery

- Add the main repository as a remote to update later::

    $ git remote add rougeth https://github.com/rougeth/bottery
    $ git fetch rougeth

- Create a `virtualenv`_.
- Install Bottery in editable mode with development dependencies::

    $ pip install -e ".[dev]"

.. _GitHub account: https://github.com/join
.. _latest version of git: https://git-scm.com/downloads
.. _username: https://help.github.com/articles/setting-your-username-in-git/
.. _email: https://help.github.com/articles/setting-your-email-in-git/
.. _Fork: https://github.com/rougeth/bottery#fork-destination-box
.. _Clone: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork
.. _virtualenv: http://docs.bottery.io/en/latest/installation.html#virtualenv


Development
-----------

Use PEP-8 for code style and `isort <https://pypi.python.org/pypi/isort>`_ to sort your imports.

Bottery uses `tox <http://tox.readthedocs.io>`_ for testing and general development.

After ``tox`` is installed, just execute::

    $ tox

To run all tests in all supported Python versions and lint checks.

If you want to run a specific test in a specific environment, you can also execute::


    $ tox -e py36 -- tests/test_cli.py


Documentation
-------------

Documentation updates or fixes are welcome. To generate docs locally, execute::

    $ tox -e docs

