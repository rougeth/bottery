# bottery
:battery: A framework for building bots

[![Build Status](https://travis-ci.org/rougeth/bottery.svg?branch=master)](https://travis-ci.org/rougeth/bottery)
[![Build status](https://ci.appveyor.com/api/projects/status/we3h64nj98vvxcre/branch/master?svg=true)](https://ci.appveyor.com/project/rougeth/bottery/branch/master)
[![PyPI](https://img.shields.io/pypi/v/bottery.svg)](https://pypi.python.org/pypi/bottery)

* [Usage](#usage)
  * [Installing](#installing)
  * [Creating a project](#creating-a-project)
  * [Configuring Telegram](#configuring-telegram)
  * [Running](#running)
* [Development](#development)

## Usage

### Installing
```bash
$ pip install bottery
```

### Creating a project
```bash
$ bottery startproject librarybot
```

This will create a librarybot directory in your current directory with three files inside:

```bash
librarybot/
    __init__.py
    patterns.py
    settings.py
```

- The outer **librarybot/** root directory is just a container for your project. Its name doesn’t matter to Bottery; you can rename it to anything you like.
- **librarybot/\_\_init\_\_.py**: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs;
- **librarybot/patterns.py**: The Pattern declarations for this Bottery project;
- **library/settings.py**: Settings/configuration for this Bottery project.

### Configuring Telegram
We can get new messages from two different ways: defining a webhook with SSL implemented on Telegram or through polling. For now, Bottery implements the first way and because of that you need to define a valid and accessible externally hostname on settings.py:

```python
# settings.py
HOSTNAME = 'mybot.example.com'
```

If you're developing or testing your bot, you can use a tunnel to expose Bottery. Services like [ngrok](https://ngrok.com/) helps a lot to do that.

Bottery register the telegram webhook url (that uses the `HOSTNAME` variable on settings) and Telegram uses that url send the new messages that your bot receives.

The Bottery setup with ngrok is simple. Once it is [installed](https://ngrok.com/download), run `$ ngrok http 8000` (if you need help running ngrok, check [its documentation](https://ngrok.com/docs). This command will give you two urls (`http` and `https`) of the created tunnel. Get the hostname (full url without `https://` part) and fill `HOSTNAME` on `settings.py`.

Now, you just need to get your bot token the fill on `settings.py`:

```python
# settings.py
PLATFORMS = {
    'telegram': {
        'ENGINE': 'bottery.platform.telegram',
        'OPTIONS': {
            'token': 'your-token-here',
        }
    },
}
```

### Running
```bash
$ bottery run --debug
```

## Development

Please see [our contribution guide](CONTRIBUTING.rst).




