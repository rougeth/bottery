import logging
import logging.config
import os
from unittest import mock

import click
from click.testing import CliRunner

from bottery.cli import cli, debug_option, run


@mock.patch('bottery.cli.App.run')
def test_app_run_is_called(mocked_run):
    runner = CliRunner()
    runner.invoke(run)
    assert mocked_run.called


def test_debug_flag_enabled():
    logger = logging.getLogger('bottery')
    logger.setLevel(logging.INFO)

    @click.command()
    @debug_option
    def hello(debug):
        pass

    runner = CliRunner()
    runner.invoke(hello, ['--debug'])

    assert logger.level == logging.DEBUG


def test_debug_flag_disabled():
    logger = logging.getLogger('bottery')
    logger.setLevel(logging.INFO)

    @click.command()
    @debug_option
    def hello(debug):
        pass

    runner = CliRunner()
    runner.invoke(hello)

    assert logger.level == logging.INFO


def test_startproject():
    runner = CliRunner()
    with runner.isolated_filesystem():
        project_name = 'librarybot'
        project_files = ['patterns.py', 'settings.py']

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
