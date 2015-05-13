import codecs
import json
import csv

#54f14ea2e4b0c7427aeaa17f

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

from relateiq.client import RelateIQ
from relateiq.lists import List
from relateiq.contacts import Contact

def main() :
	RelateIQ("554bd961e4b0957bd04218f3", "75NyjX91ZvyX9hSUrkjSwFCdp3L")
	listObj = List("54f14ea2e4b0c7427aeaa17f")

	x1 = 0
	x2 = x1 + 150

	while True:

		listItems = listObj.ListItems.fetchPage(x1,x2)

		if not listItems:
			break

		file = codecs.open('test.csv', 'a+', encoding='utf8')

		for x in listItems:
			for key, value in x.fieldValues().iteritems():
				if (key == u'58'):
					file.write(value + '\n')

			print x.name()

		x1 = x2
		x2 = x1 + 150

	#for x in listItems:
		#item = x.get('fieldValues')
		#.get('58', None).get('raw', None)
		#print item
		#item = x['fieldValues']['58']['raw']
		#file.write(item + '\n')

	#print listItems

	#data = json.loads(listItems)

	#with open('test.csv', 'w') as fp:
		#f = open('test.txt', 'r+')
		#f.write("" + listItems)

		#with open('test.txt', 'w') as outfile:
			#json.dump(listItems, outfile)

		#csv_file = csv.writer(fp, delimiter=',')
		#csv_file.writerows([listItems])

		#csv_file = csv.writer(fp)
		#for item in data:
			#csv_file.writerow(item)

main()