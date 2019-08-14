#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os

# Get current working directory
CWD = os.getcwd()

# URLs
URL_BASE  = 'https://www.technomarin.ru/'
URL_MANUF = URL_BASE  + 'index.php?route=product/manufacturer'

# Files
OUTPUT_FOLDER = os.path.join(CWD, 'data')
OUTPUT_MANUF  = os.path.join(OUTPUT_FOLDER, 'manufacturers.json')
OUTPUT_GOODS  = os.path.join(OUTPUT_FOLDER, 'goods.json')
OUTPUT_REPORT = os.path.join(OUTPUT_FOLDER, 'report.json')

# Log
LOG_FILE = os.path.join(CWD, 'log')

# Prograss bar
BAR_FILL  = '█'
BAR_EMPTY = '-'

# Help infomration
VERSION = '2.0.0'
DESCRIPTION = '''
Technomarin scraper is a script written in Python that
scrapes and saves information about manufacturers and
their goods from https://technomarin.ru
'''
EPILOG = '''
version: {}
 author: Solovyev Aleksey <solovyev.a@icloud.com>
'''.format(VERSION)

# Check folder existence
try:
    os.makedirs(OUTPUT_FOLDER)
except:
    pass
