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
@click.option('--settings')
@click.argument('plataform', required=False)
def run(settings, plataform):
    # .py vs init config file
    # Check how Lektor discover settings files
    # https://github.com/lektor/lektor/blob/master/lektor/project.py#L67-L79
    from batteries.conf import settings

    if not plataform:
        return run_them_all(settings.PLATAFORMS)

    plataform = settings.PLATAFORMS[plataform]
    engine = importlib.import_module(plataform['ENGINE'])
    engine.run(**plataform['OPTIONS'])
    return 0



def run_them_all(plataforms):
    '''Run every plataform configured on settings.py'''

    from subprocess import list2cmdline
    from honcho.manager import Manager

    daemons = []
    for plataform in plataforms:
        daemons += [
            (plataform, ['batteries', 'run', plataform]),
        ]

    manager = Manager()
    for name, cmd in daemons:
        manager.add_process(
            name,
            list2cmdline(cmd),
            quiet=False,
        )
    manager.loop()
    sys.exit(manager.returncode)
