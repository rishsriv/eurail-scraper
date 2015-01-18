from lxml import html
from splinter.browser import Browser
import csv

browser = Browser()

f = open('in.csv')
output = []
reader = list(csv.DictReader(f))
for row in reader[15:16]:
	cities = row['City Pairs']
	cities = cities.replace('Haarlemmermeer', 'Amsterdam ')
	cities = cities.split('-')
	dates = ['07/26/2014', '07/29/2014', '08/03/2014']
	for date in dates:
		browser.visit('http://www.raileurope.com/index.html')
		browser.fill('from0', cities[0])
		browser.fill('to0', cities[1])
		browser.fill('deptDate0', date)
		browser.find_by_id('fs-submit').first.click()

		a = browser.html
		a = a.encode('utf8')
		a = a.replace('<a class="cat1">', 'Economy')
		a = a.replace('<a class="cat2">', 'Comfort')
		a = a.replace('<a class="cat3">', 'Premier')
		
		doc = html.document_fromstring(a)
		trains = doc.cssselect('div.tiered-row.shadowbox')
		if len(trains) > 0:
			for train in trains:
				l = []
				l.append(date)
				l.append(cities[0])
				l.append(cities[1])
				details = train.text_content()
				details = details.split('\n')
				for i in xrange(len(details)):
					details[i] = details[i].strip()
					details[i] = details[i].lstrip()
				details = [i for i in details if i != '']
				for detail in details:
					l.append(detail)
				output.append(l)
		else:
			l = []
			l.append(date)
			l.append(cities[0])
			l.append(cities[1])
			l.append('error')
			output.append(l)
		print 'Processed', cities, date
	g = open('final_output_' + str(cities) + '.csv', 'wb')
	writer = csv.writer(g)
	writer.writerows(output)
	g.close()
	'Processed', cities

f.close()