import requests
import urllib.request
import time
import csv

from datetime import datetime
from bs4 import BeautifulSoup

# constants used in code
BASE_URL = 'https://www.amazon.ae'
NOT_FOUND = 'None'
INCREMENT_ONE = 1
SLEEP_SEC = 1

# create file with time attached to it for safty purposes
fHandle = open('csvFileCreatedAt-' + datetime.now().strftime('%H-%M-%S') + '.csv', 'w')

# write in file
def writeFile(data):
	csvWriter = csv.writer(fHandle)
	csvWriter.writerow(data)

# get html of the provided url page
def getHtml(url):
	try:
		response = requests.get(url)
	except Exception as e:
		print('Oops! Something went worng fetching the link - ' + format(e))
	return BeautifulSoup(response.text, 'html.parser')

# iterate through the fetched links get price and place in the file
def iterateLinks(subLinks):
	for link in subLinks:
		data = []
		html = getHtml(BASE_URL + link.get('href'))
		try:
			asin = html.find('input', {'id':'ASIN'})
			if str(asin) != NOT_FOUND:
				asin = asin.get('value')
			else:
				asin = 'ASIN Not Found'
			title = html.find('span', {'id':'productTitle'}).get_text().strip()
			if str(html.find('span', {'id':'priceblock_ourprice'})) != NOT_FOUND:
				price = html.find('span', {'id':'priceblock_ourprice'}).get_text().split('AED')[1]

			if str(html.find('span', {'id':'priceblock_saleprice'})) != NOT_FOUND:
				price = html.find('span', {'id':'priceblock_saleprice'}).get_text().split('AED')[1]

			bullets = (html.find('div', {'id':'feature-bullets'}))
			if str(bullets) != NOT_FOUND:
				bullets = bullets.find_all('span', {'class':'a-list-item'})
			else:
				bullets = []
			description = (html.find('div', {'id':'productDescription'}))
			if str(description) != NOT_FOUND:
				description = description.find_all('span', {'class':'a-list-item'})
			else:
				description = []

			data.append(asin)
			data.append(title)
			data.append(price)
			if bullets:
				for l in range(5):
					try:
						data.append(bullets[l].get_text().strip())
					except:
						data.append('')
			else:
				for l in range(5):
					try:
						data.append(description[l].get_text().strip())
					except:
						data.append('')

			text = ''
			for l in description:
				text += l.get_text().strip()

			data.append(text)
			images = (html.find('div', {'id':'altImages'})).find_all('img')
			for l in range(len(images) - 1):
				data.append(images[l].get('src').split('._')[0] + '._SS400_.jpg')
			writeFile(data)
		except Exception as e:
			print('		>> Entry missed due to some error from this link = ' + BASE_URL + link.get('href'))
			print('		>> ERRROR = ' + format(e))
			print(' 	==========')

# input for user
enteredUrl = input('Please Enter Starting Point for Scrapper: ')
startUrl = enteredUrl.split('&page=')[0]
print('=== Starting Scrapping ===')
writeFile([
	'ASIN',
	'NAME',
	'PRICE',
	'BULLET 1',
	'BULLET 2',
	'BULLET 3',
	'BULLET 4',
	'BULLET 5',
	'DESCRIPTION'
])
try:
	count = int(enteredUrl.split('&page=')[1][0])
except:
	count = 1

while count <= 50:
	html = getHtml(startUrl + '&page=' + str(count))
	links = html.find_all('a', {'class':'a-link-normal a-text-normal'})
	if str(links) == NOT_FOUND:
		break
	iterateLinks(links)
	print(str(count) + ' == Pages Done')
	count += INCREMENT_ONE
	time.sleep(SLEEP_SEC)

# close file
fHandle.close()
print('=== Scrapping Finished ===')