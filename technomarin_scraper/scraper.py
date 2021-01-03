#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import json
import re
from datetime       import datetime
from lxml           import html
from .constants     import URL_MANUF, OUTPUT_MANUF, OUTPUT_GOODS, OUTPUT_REPORT
from .logger        import logging_decorator, logger
from .progress_bar  import progress_bar
try:
    from urllib.request import urlopen
    from urllib.error   import URLError, HTTPError
except ImportError:
    from urllib2        import urlopen, URLError, HTTPError


class TechnomarinScraper():
    """
    Receive and parse information on manufacturers
    and products from the Technomarin(https://www.technomarin.ru) website
    """

    def __init__(self):
        """ Scraper initializations"""
        try:
            logger.info('Last update on {}'.format(self.__readFile__(OUTPUT_REPORT).get('lastUpdate', '')))
        except FileNotFoundError:
            logger.info('No previous updates found')

    def __writeFile__(self, file, data):
        """ Write data to a file """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def __readFile__(self, file):
        """ Read data from a file """
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __getHTML__(self, url):
        """ Fetch page content(DOM tree) """
        try:
            return html.fromstring(urlopen(url).read())
        except KeyboardInterrupt:
            return None
        except HTTPError as error:
            logger.error('The server couldn\'t fulfill the request. Error code: {}'.format(error.code))
            sys.exit(1)
        except URLError as error:
            logger.error(error.reason)
            if error.reason.errno == 11001:
                logger.info('Please check your internet connection or try again later')
            sys.exit(1)
        except:
            logger.exception('¯\\_(ツ)_/¯')
            sys.exit(1)

    def __getProductInfo__(self, product_page):
        """ Return information from the product page """
        title = product_page.xpath('.//div[@class="tm-product-name-container"]/a')[0]
        return {
            'code':     product_page.xpath('.//div[@class="tm-product-description-container"]//p/text()')[0].split(': ')[1],
            'name':     title.get('title'),
            'url':      title.get('href'),
            'image':    product_page.xpath('.//div[@class="img-container"]/img[1]/@src')[0],
            'price':    float(re.sub('[^0-9]', '', product_page.xpath('.//span[contains(@class, "general-price")]/text()')[0])) / 100,
            'in_stock': True if len(product_page.xpath('.//span[@class="goods-available"]')) > 0 else False
        }

    @logging_decorator
    def getManufacturers(self):
        """ Get a list of all manufacturers and save it """
        logger.info('Getting manufacturers')

        DOM = self.__getHTML__(URL_MANUF)
        links = DOM.xpath('//div[@id="content"]//div[@class="row"]//a')

        manufacturers = {}
        for link in links:
            manufacturers[link.text if link.text is not None else 'common'] = link.get('href')

        self.__writeFile__(OUTPUT_MANUF, manufacturers)

        logger.info('{} manufacturers were received'.format(len(links)))
        return manufacturers

    @logging_decorator
    def getGoods(self):
        """ Get a list of goods of each manufacturer and save it """
        try:
            manufacturers = self.__readFile__(OUTPUT_MANUF)
        except FileNotFoundError:
            logger.warning('List of manufacturers not found')
            manufacturers = self.getManufacturers()

        logger.info('Getting goods')
        goods           = {}
        number_of_goods = 0
        number_of_manuf = len(manufacturers.keys())
        current_manuf   = 0

        # Parse information
        for name, url in manufacturers.items():
            current_manuf += 1
            current_page   = 0
            goods[name]    = []

            progress_bar(number_of_manuf, current_manuf)

            while True:
                current_page += 1
                DOM = self.__getHTML__('{}&limit=100&page={}'.format(url, current_page))

                # Catch user interrupt
                if DOM is None: break

                products = DOM.xpath('//div[contains(@class, "tm-product-container")]')

                if len(products) == 0: break

                for product in products:
                    number_of_goods += 1
                    goods[name].append(self.__getProductInfo__(product))

            # Catch user interrupt
            if DOM is None: break

        sys.stdout.write('\n')
        logger.info('{} entries were received'.format(number_of_goods))
        self.__writeFile__(OUTPUT_GOODS, goods)
        self.report(number_of_manuf, number_of_goods)
        return goods

    @logging_decorator
    def report(self, number_of_manuf=None, number_of_goods=None):
        """ Write general information on manufacturers and their products """
        logger.info('Creating report')
        report = {
            'number_of_manufacturers': number_of_manuf,
            'number_of_goods':         number_of_goods,
            'lastUpdate':              datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
        self.__writeFile__(OUTPUT_REPORT, report)
        logger.info('Report was created')
        return report
