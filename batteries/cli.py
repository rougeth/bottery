import importlib
import os
import sys

import click


'''
╔═════════╗
╠batteries╠
╚═════════╝
'''


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
    settings_files = open(os.path.join(project_dir, 'batteries.py'), 'w')
    settings_files.close()


@cli.command('run')
@click.option('--port', default=8000, type=int)
def run(port):
    '''
    Run a web server to handle webhooks requests from all plataforms
    configured on the project settings.
    '''
    # .py vs init config file
    # Check how Lektor discover settings files
    # https://github.com/lektor/lektor/blob/master/lektor/project.py#L67-L79
    from aiohttp import web

    from batteries.conf import settings

    app = web.Application()

    plataforms = settings.PLATAFORMS.values()
    for plataform in plataforms:
        mod = importlib.import_module(plataform['ENGINE'])
        engine = mod.engine(**plataform['OPTIONS'])
        engine.configure()

        app.router.add_route('POST', engine.path, engine.handler)

    web.run_app(app, port=port)
