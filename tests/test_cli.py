import os

from click.testing import CliRunner

import bottery
from bottery.cli import cli


def test_startproject():
    runner = CliRunner()
    with runner.isolated_filesystem():
        project_name = 'librarybot'
        project_files = ['bot.py', 'settings.py']

        result = runner.invoke(cli, ['startproject', project_name])

        assert result.exit_code == 0
        assert os.listdir() == [project_name]
        assert sorted(os.listdir(project_name)) == sorted(project_files)


def test_startproject_invalid_project_name():
    runner = CliRunner()
    with runner.isolated_filesystem():
        project_name = 'library-bot'
        result = runner.invoke(cli, ['startproject', project_name])

    assert result.exit_code == 2


def test_version_option():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])

    assert bottery.__version__ in result.output
    assert result.exit_code == 0

