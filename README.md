# bottery
:battery: A framework for building bots


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


### Running
```bash
$ bottery run
```
