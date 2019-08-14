#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
PY_VERSION = sys.version_info
if (PY_VERSION >= (3, 0)):
    from technomarin_scraper import TechnomarinScraper, args, logger
else:
    from technomarin_scraper import logger
    logger.error('This script requires Python 3.x! Your version is {}.{}'.format(PY_VERSION[0], PY_VERSION[1]))
    sys.exit(1)

def main():
    logger.info('START SCR')

    scraper = TechnomarinScraper()
    if args.goods and not args.manufacturers:
        scraper.getGoods()
    elif args.manufacturers and not args.goods:
        scraper.getManufacturers()
    else:
        scraper.getManufacturers()
        scraper.getGoods()

    logger.info('EXIT SCR')

if __name__ == '__main__':
    main()
