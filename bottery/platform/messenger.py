# isort:skip_file
# flake8: noqa
import warnings
from bottery.exceptions import BotteryDeprecationWarning

warnings.warn('Module `bottery.platform.messenger` is deprecated, '
             'use `bottery.messenger` instead',
             BotteryDeprecationWarning, stacklevel=2)

from bottery.messenger import *
