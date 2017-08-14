import os

import click


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
def run(settings):
    # .py vs init config file
    # Check how Lektor discover settings files
    # https://github.com/lektor/lektor/blob/master/lektor/project.py#L67-L79

    here = os.getcwd()

    if settings:
        file_exists = os.path.isfile(settings)
    else:
        file_exists = os.path.isfile(os.path.join(here, 'batteries.py'))

    if file_exists:
        click.secho('batteries.py found!', fg='green')
    else:
        click.secho('batteries.py not found!', fg='red')
