import logging.config
import os
import shutil
import sys
from importlib import import_module

import click

import bottery
from bottery import Bottery
from bottery.log import DEFAULT_LOGGING

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger('bottery')


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    """Bottery"""

    # If no subcommand was given and the version flag is true, shows
    # Bottery version
    if not ctx.invoked_subcommand and version:
        click.echo(bottery.__version__)
        ctx.exit()

    # If no subcommand but neither the version flag, shows help message
    elif not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
        ctx.exit()


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


def import_string(import_name):
    try:
        module_name, obj_name = import_name.rsplit('.', 1)
    except ValueError:
        module_name = import_name
        obj_name = 'bot'

    base = os.getcwd()
    sys.path.insert(0, base)

    try:
        module = import_module(module_name)
    except Exception as e:
        raise e

    try:
        return getattr(module, obj_name)
    except AttributeError as e:
        raise ImportError(e)


@cli.command('run')
@click.option('--bot-module', default='bot', type=str)
@click.option('--port', default=7000, type=int)
def run(bot_module, port):
    bot = Bottery()

    try:
        bot.run(server_port=port)
    except KeyboardInterrupt:
        bot.stop()
