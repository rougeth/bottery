import logging
import logging.config
import os

import click
from click.testing import CliRunner
from testfixtures import LogCapture

from bottery.cli import cli, debug_option
from bottery.log import ColoredFormatter, DEFAULT_LOGGING


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


def test_ColoredFormatter():
    c = ColoredFormatter()
    expected = [
        'DEBUG',
        '\x1b[34mINFO\x1b[0m',
        '\x1b[33mWARN\x1b[0m',
        '\x1b[31mERROR\x1b[0m',
        '\x1b[30m\x1b[41mCRITICAL\x1b[0m'
    ]
    logging.config.dictConfig(DEFAULT_LOGGING)
    with LogCapture(names='bottery') as l:
        logger = logging.getLogger('bottery')
        logger.debug('DEBUG')
        logger.info('INFO')
        logger.warning('WARN')
        logger.error('ERROR')
        logger.critical('CRITICAL')
        records = [x for x in l.records]
        for i in range(len(records)):
            assert c.format(records[i]) == expected[i]
