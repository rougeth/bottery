import logging.config
import os
import shutil

import click

import bottery
from bottery.app import App
from bottery.log import DEFAULT_LOGGING

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger('bottery')


def debug_option(f):
    @click.option('--debug/--no-debug', default=False)
    def wrapper(*args, **kwargs):
        if kwargs.get('debug', False):
            logger.setLevel(logging.DEBUG)
        return f(*args, **kwargs)

    return wrapper


@click.group()
def cli():
    """Bottery"""


@cli.command('startproject')
@click.argument('name')
def startproject(name):
    # Must validate projects name before creating its folder
    if not name.isidentifier():
        message = ('"{name}" is not a valid project name. Please make sure '
                   'the name is a valid identifier.')
        raise click.BadParameter(message.format(name=name))

    project_dir = os.path.join(os.getcwd(), name)
    os.mkdir(project_dir)

    # There's probably a better way to do this :)
    template_dir = os.path.join(bottery.__path__[0], 'conf/project_template')
    for root, dirs, files in os.walk(template_dir):
        for filename in files:
            new_filename = filename[:-4]  # Removes "-tpl"
            src = os.path.join(template_dir, filename)
            dst = os.path.join(project_dir, new_filename)
            shutil.copy(src, dst)


@cli.command('run')
@click.option('--port', default=8000, type=int)
@debug_option
def run(port, debug):
    app = App()
    app.run()
