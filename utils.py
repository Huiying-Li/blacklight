"""Python utility functions.

Python utility functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import config
import logging

def get_logger():
    logger = logging.getLogger('normal')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s %(pathname)s:%(lineno)d %(levelname)s]: %(message)s','%H:%M:%S,%m/%d')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger    
