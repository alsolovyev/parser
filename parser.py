#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from time import sleep
import csv
from random import uniform

url = 'http://www.technomarin.ru/index.php?route=product/manufacturer'

class bcolors:
    NAME = '\033[36m'
    GREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'

def get_html(url):
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, 'lxml')
	return soup

def get_all_companys(html):
	list_of_ocmpanys = []
	i = 0
	a = 0
	div = html.find('div', id='content')

	rows = div.find_all('div', class_='row')

	for row in rows:
		i = i + 1
		links = row.find_all('a')
		for link in links:
			a = a + 1
			url = link.get('href') + '&limit=100'
			name = link.next
			#print(url)
			#print(name)

			list_of_ocmpanys.append({
				'name': name,
				'url': url,
				})
	for item in list_of_ocmpanys:
		print(item['name'])
		print(item['url'])
		print('**************************************************************************************')
	print('cunt rows: ' + str(i))
	print('count links: ' + str(a))
	print('\n')
	return list_of_ocmpanys

def get_pages_number(html):
	try:
		try:
			r = requests.get(html)
			html = r.text
			soup = BeautifulSoup(html, 'lxml')
		except:
			r = requests.get(html)
			html = r.text
			soup = BeautifulSoup(html, 'lxml')

			
		div = soup.find('div', id='content')
		ls = div.find_all('li')[-1].find('a').get('href').split('page=')
		pages = int(ls[1])
	except:
		pages = 1

	print("TOTAL PAGES: " + str(pages))
	return pages


def get_all_products(url, pages):
	#list of companys(list)
	#total_urls = parser.get_all_companys()

	products = []
	i = 0
	#get request got item in total_urls
	while (pages > 0):
		new_url = url + '&page=' + str(pages)
		pages = pages - 1
		print(new_url)
		try:
			r = requests.get(new_url)
			html = r.text
			soup = BeautifulSoup(html, 'lxml')
		except:
			print(bcolors.WARNING + 'Trying again. Error code: 1' + bcolors.ENDC)
			r = requests.get(new_url)
			html = r.text
			soup = BeautifulSoup(html, 'lxml')

			
		div = soup.find_all('div', class_='tm-product-container')
		for item in div:
			headers = item.find_all('div', class_='tm-product-name-container')
			for head in headers:
				i = i + 1 
				link = head.find('a').get('href')
				products.append(link)


	return products


	# "for i in range(1, total_pages):"
	# # 
def get_data(html, count):
	while(True):
		try:
			r = requests.get(html)
			r = r.text
			soup = BeautifulSoup(r, 'lxml')
		except:
			continue
			print(bcolors.FAIL + 'Trying again. Error code: 1' + bcolors.ENDC)
		break
	#*****************manufacturer******************
	try:
		manufacturer = soup.find('a', class_='manufacturer').text.replace('\n', '').strip()
	except:
		manufacturer = ''		

	#******************categories***********************
	ul = soup.find('ul', class_='breadcrumb')
	#main category
	cat = ul.find_all('li')[3:4]
	for i in cat:
		cat = i.getText().strip()
		# print(cat)

	#second category
	cat1 = ul.find_all('li')[4:5]
	for i in cat1:
		cat1 = i.getText().strip()

	#second category
	cat2 = ul.find_all('li')[5:6]
	for i in cat2:
		cat2 = i.getText().strip()
	#third category
	cat3 = ul.find_all('li')[6:7]
	for i in cat3:
		cat3 = i.getText().strip()
	#***************************************************
	name = soup.find('h1').getText()
	#***************************************************
	img = soup.find('a', class_='thumbnail').get('href')
	#******************description**********************
	try:
		div = soup.find('div', class_='tm-product-info-container')
		description = div.find('p').get_text().replace('\n', ' ').replace(';', ' ')
	except:
		description = ''
	#******************price**********************
	price = soup.find('div', class_='tm-product-price-container').find('span', class_='general-price').getText().replace('\n', '').strip().split(' ')
	#******************available**********************
	available = soup.find('div', class_='tm-product-stock-container').find('span').get('class')
	if (available[0] == 'goods-available'):
		available = '+'
	else:
		available = '-'
	#******************article**********************
	article = soup.find('div', class_='tm-model-container').getText().strip().split(' ')

	if (cat3 == name):
		cat3 = ''
	else:
		pass
	#available in shop
	a = '+'

	# print(cat)
	# print(cat1)
	# print(cat2)
	# print(cat3)
	# print('*************')
	# print(article[1])
	# print('*************')
	# print(available)
	# print('*************')
	# print(price[0])
	# print('*************')
	# print(description)
	# print('*************')

	print('       ' + bcolors.WARNING + str(count) + bcolors.ENDC + '. ' + name)
	with open('products.csv', 'a') as file:
		writer = csv.writer(file)
		writer.writerow((cat, cat1, cat2, cat3, name, a, description, price[0], manufacturer, img, article[1], available))
	
	# sleep(uniform(1, 2))


def main():
	with open('products.csv', 'w') as file:
		writer = csv.writer(file)
										# writer.writerow((cat, cat1, cat2, cat3, name, a, description, price[0], manufacturer, img, article[1], available))
		writer.writerow(('Категория', 'Подкатегория 1', 'Подкатегория 2', 'Дополнительные категории', 'Наименование', 'Отображать в моем магазине', 'Описание', 'Цена, р.', 'Производитель', 'Фотографии', 'Код продавца товара', 'Остаток'))
	#error counter
	pr = 0
	er = 0
	#получаем страницу компании(список)
	html = get_html(url)
	# получаем список всех компаний
	list_of_companys = get_all_companys(html)
	for name in list_of_companys:
		print('')
		print("***************************************")
		print("Название комании: " + bcolors.NAME + str(name['name'] + bcolors.ENDC))
		local_html = name['url'];
		#print(local_html)
		# r = requests.get(local_html)
		# html = r.text
		# soup = BeautifulSoup(html, 'lxml')
		# получаяем количество страниц продукта
		# try:
		total_pages = get_pages_number(local_html)
		#получаем список всех продурктов
		list_of_products = get_all_products(local_html, total_pages)
		for index,link in enumerate(list_of_products):
			get_data(str(link), index+1)
			pr = pr + 1
		# except:
		# 	er = er + 1
		# 	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		# 	print('XXXXXXXXXXXXXerrrrrorrrrXXXXXXXXX')
		# 	print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		# 	total_pages = get_pages_number(local_html)
		# 	#получаем список всех продурктов
		# 	list_of_products = get_all_products(local_html, total_pages)
		# 	for link in list_of_products:
		# 		get_data(str(link))


		# with open('items.txt', 'a') as file:
		# 	for item in list_of_products:
		# 		file.write(item + '\n')

	print('')
	print('*****************************')
	print('            DONE')
	print('*****************************')
	print('Products found: ' + str(pr))
	print(er)
	input(bcolors.WARNING + 'Press Enter to continue...' + bcolors.ENDC)





if __name__ == '__main__':
	main()


#15:00