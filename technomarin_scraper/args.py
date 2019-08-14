#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse
from .constants import DESCRIPTION, EPILOG, VERSION

# Create a new ArgumentParser object
argsParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=DESCRIPTION,
                                     epilog=EPILOG)
argsParser.version = VERSION # add version

# Add arguments
argsParser.add_argument('-v', '--version', action='version')
argsParser.add_argument('-m', '--manufacturers', action='store_true',
                        help='Scrape and save information only about manufacturers')
argsParser.add_argument('-g', '--goods', action='store_true',
                        help='Scrape and save information only about goods')

# Init parser
args = argsParser.parse_args()
