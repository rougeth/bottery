import logging
from unittest import mock

import pytest
from testfixtures import LogCapture

from bottery.log import DEFAULT_LOGGING, ColoredFormatter, Spinner


def test_formatter():
    """Test if logs are being colored"""

    logging.config.dictConfig(DEFAULT_LOGGING)

    with LogCapture(names='bottery') as logs:
        logger = logging.getLogger('bottery')
        logger.debug('DEBUG')
        logger.info('INFO')
        logger.warning('WARN')
        logger.error('ERROR')
        logger.critical('CRITICAL')
        records = [record for record in logs.records]

    # Create a list of all records formated with ColoredFormatter
    colored_formatter = ColoredFormatter()
    formatted_records = [colored_formatter.format(record)
                         for record in records]

    expected_records = [
        'DEBUG',
        'INFO',
        '\x1b[33mWARN\x1b[0m',
        '\x1b[31mERROR\x1b[0m',
        '\x1b[30m\x1b[41mCRITICAL\x1b[0m'
    ]

    assert formatted_records == expected_records


@mock.patch('bottery.log.Halo')
def test_spinner_instance(mocked_halo):
    Spinner('message')
    mocked_halo.assert_called_once_with(text='message', spinner='dot',
                                        color='green')


@pytest.mark.parametrize('attr', ['__enter__', '__exit__'])
@mock.patch('bottery.log.Halo')
def test_spinner_context(mocked_halo, attr):
    spinner = Spinner('message')
    with spinner:
        pass

    assert getattr(spinner.halo, attr).call_count == 1
