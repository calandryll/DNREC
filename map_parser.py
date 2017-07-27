# /usr/local/bin/python
import csv

map = 'mapping.txt'

wfile = list(csv.reader(open(map, 'rU'), delimiter = '\t'))

for records in wfile:
	print records[1][2]