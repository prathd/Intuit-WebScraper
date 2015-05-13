import codecs
import json
import string
import csv

#54f14ea2e4b0c7427aeaa17f

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

from relateiq.client import RelateIQ
from relateiq.lists import List
from relateiq.contacts import Contact
from relateiq.listitem import ListItem

from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        self.seen = set()
        self.seenN = set()
        self.seenC = set()

        RelateIQ("554bd961e4b0957bd04218f3", "75NyjX91ZvyX9hSUrkjSwFCdp3L")
        listObj = List("54f14ea2e4b0c7427aeaa17f")

        x1 = 0
        x2 = x1 + 150

        while True:

            listItems = listObj.ListItems.fetchPage(x1,x2)

            if not listItems:
                break

            for x in listItems:
                for key, value in x.fieldValues().iteritems():
                    if (key == u'58'):
                        self.seen.add(value)
                    if (key == u'51'):
                        self.seenC.add(value.lower())

                t = x.name()
                t = t.lower()

                self.seenN.add(t)


            x1 = x2
            x2 = x1 + 150

            print self.seenC
            print self.seenN

    def process_item(self, item, spider):
        email = item['email']
        email = email.lower()

        tempName = item['firstName'] + " " + item['lastName']
        compName = item['companyName']

        drop = False

        if email in self.seen:
            raise DropItem('Duplicate email found %s' % email)
            drop = True

        if tempName in self.seenN:
            if compName in self.seenC:
                raise DropItem('Duplicate NAME OR EMAIL found %s, %s', tempName, compName)
                drop = True

        abc = "0"

        if item['qbo'] == "FALSE":
            abc = "1"

        if not drop:
            contact = Contact()
            contact.name(string.capwords(tempName))
            contact.email(email)
            contact.phone([item['phoneNumber']])
            contact.company(string.capwords(item['companyName']))
            contact.create()

            listObj = List("54f14ea2e4b0c7427aeaa17f")
            listItem = ListItem(parent = listObj)
            listItem.contactIds([contact.id()])
            listItem.name(string.capwords(contact.name()))
            listItem.fieldValues({"61":"2","58":contact.email(),"51":contact.company(),"72":"0","87":"1","100":abc})
            listItem.create()

        self.seen.add(email)
        self.seenC.add(compName)
        self.seenN.add(tempName)

        return item