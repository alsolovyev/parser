#!/usr/bin/env python3
# -*- coding: utf8 -*-

# import os
import sys
import logging
from functools  import wraps
from .constants import LOG_FILE

# Create an instance of logger
logger = logging.getLogger('parser')
logger.setLevel(logging.INFO)

logFormat = logging.Formatter('%(asctime)s - %(name)s[%(levelname)s] - %(message)s', "%Y-%m-%d %H:%M:%S")

# Write logs to a file
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logFormat)
logger.addHandler(fileHandler)

# Write logs to the console
consoleHandler = logging.StreamHandler(sys.stderr)
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormat)
logger.addHandler(consoleHandler)

# Decorator
def logging_decorator(func):
    @wraps(func)
    def wrapper(*args):
        # logger.info('Start')
        return func(*args)
        # logger.info('End')
    return wrapper
