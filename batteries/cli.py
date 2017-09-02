import importlib
import logging.config
import os
import sys

import click

from batteries.log import DEFAULT_LOGGING


logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger('batteries')


'''
╔═════════╗
╠batteries╠
╚═════════╝
'''

def debug_option(f):
    @click.option('--debug/--no-debug', default=False)
    def wrapper(*args, **kwargs):
        if kwargs.get('debug', False):
            logger.setLevel(logging.DEBUG)
        return f(*args, **kwargs)

    return wrapper


@click.group()
def cli():
    """Batteries"""


@cli.command('startproject')
@click.argument('name')
def startproject(name):
    # Must validate projects name before creating its folder
    project_dir = os.path.join(os.getcwd(), name)
    os.mkdir(project_dir)

    # Use jinja2 the settings file
    settings_files = open(os.path.join(project_dir, 'settings.py'), 'w')
    settings_files.close()


@cli.command('run')
@click.option('--port', default=8000, type=int)
@debug_option
def run(port, debug):
    '''
    Run a web server to handle webhooks requests from all plataforms
    configured on the project settings.
    '''
    # .py vs init config file
    # Check how Lektor discover settings files
    # https://github.com/lektor/lektor/blob/master/lektor/project.py#L67-L79
    from aiohttp import web

    from batteries import server
    from batteries.conf import settings

    _batteries = click.style('Batteries', fg='green')
    logger.debug('Running {} \o/'.format(_batteries))

    app = web.Application()

    plataforms = settings.PLATAFORMS.values()
    if not plataforms:
        raise Exception('No plataforms configured')

    for plataform in plataforms:
        logger.debug('Importing engine %s', plataform['ENGINE'])
        mod = importlib.import_module(plataform['ENGINE'])
        engine = mod.engine(**plataform['OPTIONS'])
        logger.debug('[%s] Configuring', engine.PLATAFORM)
        engine.configure()
        logger.debug('[%s] Ready', engine.PLATAFORM)

    app.router.add_route('POST', server.WEBHOOK_PATH, server.handler)
    logger.debug('Running server')
    web.run_app(app, port=port, print=lambda x: None)
