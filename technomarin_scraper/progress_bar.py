#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
from .constants import BAR_FILL, BAR_EMPTY

# Fix this
try:
    TERMINAL_WIDTH = os.get_terminal_size().columns - 6
except:
    TERMINAL_WIDTH = 74

def progress_bar(total, current):
    percentage = int(current * 100 / total)
    complete   = int(TERMINAL_WIDTH / 100 * percentage)
    bar        = BAR_FILL * complete + BAR_EMPTY * (TERMINAL_WIDTH - complete)

    sys.stdout.write('\r{}% {}'.format(percentage, bar))
    sys.stdout.flush()
