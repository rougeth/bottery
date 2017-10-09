import logging

from testfixtures import LogCapture

from bottery.log import DEFAULT_LOGGING, ColoredFormatter


def test_ColoredFormatter():
    '''Test if logs are being colored'''

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
