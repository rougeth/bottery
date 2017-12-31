# bottery
:battery: A framework for building bots

[![Build Status](https://travis-ci.org/rougeth/bottery.svg?branch=master)](https://travis-ci.org/rougeth/bottery)
[![Build status](https://ci.appveyor.com/api/projects/status/we3h64nj98vvxcre/branch/master?svg=true)](https://ci.appveyor.com/project/rougeth/bottery/branch/master)
[![PyPI](https://img.shields.io/pypi/v/bottery.svg)](https://pypi.python.org/pypi/bottery)
[![Versions](https://img.shields.io/pypi/pyversions/bottery.svg)](https://pypi.python.org/pypi/bottery)

```python
# quick example of a ping pong bot
from bottery import Bottery


bot = Bottery()

@bot.patterns.message('ping')
def pong(message):
    return 'pong'
```

The complete example can be seen [here](https://github.com/leportella/bottery-examples).

* [Usage](#usage)
  * [Documentation](http://docs.bottery.io)
  * [Installing](#installing)
  * [Creating a project](#creating-a-project)
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

### Running
```bash
$ bottery run
```

## Development

Please see [our contribution guide](CONTRIBUTING.rst).
