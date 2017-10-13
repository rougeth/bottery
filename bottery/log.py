import logging

import click

DEFAULT_COLORS = {
    logging.WARN: {'fg': 'yellow'},
    logging.ERROR: {'fg': 'red'},
    logging.CRITICAL: {'fg': 'black', 'bg': 'red'},
}

# See how Django change its logging confs with settings specifics.
# https://github.com/django/django/blob/master/django/utils/log.py#L64
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'bottery.server',
        }
    },
    'formatters': {
        'bottery.server': {
            'class': 'bottery.log.ColoredFormatter',
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'loggers': {
        'bottery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        options = DEFAULT_COLORS.get(record.levelno, {})

        if options:
            record.msg = click.style(record.msg, **options)

        return super().format(record)
