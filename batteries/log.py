import logging

import click


DEFAULT_COLORS = {
    logging.DEBUG: lambda msg: msg,
    logging.INFO: lambda msg: click.style(msg, fg='blue'),
    logging.WARN: lambda msg: click.style(msg, fg='yellow'),
    logging.ERROR: lambda msg: click.style(msg, fg='red'),
    logging.CRITICAL: lambda msg: click.style(msg, fg='black', bg='red'),
}

# See how Django change its logging confs with settings specifics.
#https://github.com/django/django/blob/master/django/utils/log.py#L64
DEFAULT_LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'batteries.server',
        }
    },
    'formatters': {
        'batteries.server': {
            'class': 'batteries.log.ColoredFormatter',
            'format': '%(asctime)s %(message)s',
            'datefmt': '%Y/%d/%m %H:%M:%S',
        }
    },
    'loggers': {
        'batteries': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        style = DEFAULT_COLORS[record.levelno]
        record.msg = style(record.msg)
        return super().format(record)
