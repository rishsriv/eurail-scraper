#All prices in USD
import csv
from collections import OrderedDict
import dateutil.parser

output = []
r = range(1, 9)
for i in r:
	fname = str(i) + '.csv'
	with open(fname) as f:
		reader = csv.reader(f)
		for line in reader:
			line = list(line)
			line = [i for i in line if i not in ['View', 'from', 'Comfort', 'Economy', 'Premier']]
			d = {}
			d['date'] = line[0]
			d['orig'] = line[1]
			d['dest'] = line[2]
			#print line
			if line[3].lower() == 'error':
				d['error'] = True
				d['start_time'] = ''
				d['end_time'] = ''
				d['economy_price'] = ''
				d['comfort_price'] = ''
				d['premier_price'] = ''
				d['check_again'] = False
				d['duration'] = ''
			else:
				d['start_time'] = line[3]
				d['error'] = False
				if '$' in line[-3]:
					d['economy_price'] = line[-3]
					ec_index = -3
					d['comfort_price'] = line[-2]
					d['premier_price'] = line[-1]
					d['check_again'] = False
				elif '$' in line[-2]:
					d['economy_price'] = line[-2]
					d['comfort_price'] = line[-1]
					d['premier_price'] = ''
					d['check_again'] = True
					ec_index = -2
				else:
					d['economy_price'] = line[-1]
					d['check_again'] = True
					d['premier_price'] = ''
					d['comfort_price'] = ''
					ec_index = -1
				d['end_time'] = line[ec_index-4]
				d['duration'] = str(dateutil.parser.parse(d['end_time']) - dateutil.parser.parse(d['start_time']))
				print 
			output.append(d)

ordered_fieldnames = OrderedDict([('date', None),
								('orig', None),
								('error', None),
								('dest', None),
								('start_time', None),
								('end_time', None),
								('duration', None),
								('economy_price', None),
								('comfort_price', None),
								('premier_price', None),
								('check_again', None)])

with open('processed.csv', 'wb') as f:
	writer = csv.DictWriter(f, fieldnames=ordered_fieldnames)
	writer.writeheader()
	writer.writerows(output)