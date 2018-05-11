# isort:skip_file
# flake8: noqa
import warnings
from bottery.exceptions import BotteryDeprecationWarning

warnings.warn('Module `bottery.platform` is deprecated, '
             'use `bottery.platforms` instead',
             BotteryDeprecationWarning, stacklevel=2)

from bottery.platforms import *
