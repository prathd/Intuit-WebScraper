import csv
import codecs

from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        with codecs.open('grid.csv', 'r', encoding='utf8') as f:
            self.seen = set([line.strip() for line in f])
            
        self.file = codecs.open('grid.csv', 'a+', encoding='utf8')

    def process_item(self, item, spider):
        email = item['email']
        email = email.lower()

        if email in self.seen:
            raise DropItem('Duplicate email found %s' % email)

        self.seen.add(email)
        self.file.write(email + '\n')

        return item