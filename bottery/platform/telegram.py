# flake8: noqa
import warnings
from bottery.exceptions import BotteryDeprecationWarning

warnings.warn('Module `bottery.platform.telegram` is deprecated, '
             'use `bottery.telegram` instead',
             BotteryDeprecationWarning, stacklevel=2)

from bottery.telegram import *
