import logging
import logging.config
import os

import click
from click.testing import CliRunner

from bottery.cli import cli, debug_option


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
        assert os.listdir(project_name) == project_files
