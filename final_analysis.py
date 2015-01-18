import csv
import dateutil.parser
from collections import defaultdict
from collections import OrderedDict
import numpy as np
from operator import itemgetter

input_data = defaultdict(dict)

min_dept = dateutil.parser.parse('0530')
max_arrival = dateutil.parser.parse('2230')

f = open('processed.csv')
reader = csv.DictReader(f)
for line in reader:
	city = line['orig']+'-'+line['dest']
	date = line['date']
	departure_time = dateutil.parser.parse(line['start_time'])
	arrival_time = dateutil.parser.parse(line['end_time'])
	if date not in input_data[city]:
		input_data[city][date] = {}
	if departure_time > min_dept and arrival_time < max_arrival and departure_time < arrival_time:
		if line['economy_price'] != '':
			if 'economy' not in input_data[city][date]:
				input_data[city][date]['economy'] = defaultdict(list)
			input_data[city][date]['economy']['price'].append(int(line['economy_price'][1:]))
			input_data[city][date]['economy']['duration'].append(line['duration'])
		if line['comfort_price'] != '':
			if 'comfort' not in input_data[city][date]:
				input_data[city][date]['comfort'] = defaultdict(list)
			input_data[city][date]['comfort']['price'].append(int(line['comfort_price'][1:]))
			input_data[city][date]['comfort']['duration'].append(line['duration'])
		if line['premier_price'] != '':
			if 'premier' not in input_data[city][date]:
				input_data[city][date]['premier'] = defaultdict(list)
			input_data[city][date]['premier']['price'].append(int(line['premier_price'][1:]))
			input_data[city][date]['premier']['duration'].append(line['duration'])
f.close()

output = []
for city in input_data:
	for date in input_data[city]:
		for tier in input_data[city][date]:
			min_index, min_price = min(enumerate(input_data[city][date][tier]['price']), key=itemgetter(1))
			duration = input_data[city][date][tier]['duration'][min_index]
			d = {}
			d['city'] = city
			d['date'] = date
			d['tier'] = tier
			d['min_price'] = min_price
			d['duration_with_min_price'] = duration
			output.append(d)

headers = OrderedDict([('city',None),
					('date',None),
					('tier',None),
					('min_price',None),
					('duration_with_min_price',None)])
f = open('final_output.csv', 'wb')
writer = csv.DictWriter(f, fieldnames=headers)
writer.writeheader()
writer.writerows(output)
f.close()