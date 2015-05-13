#importing useful libraries
import codecs
import json
import string

#makes working with unicode easier
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

#import the RelateIQ API
from relateiq.client import RelateIQ
from relateiq.lists import List
from relateiq.contacts import Contact
from relateiq.listitem import ListItem

#import the function to Drop the Scraping of an Item
from scrapy.exceptions import DropItem

#Once given a new element from ProAdvisor, scans the RelateIQ
#    database for any duplicates based on email, name, and/or
#    company. If match, Item is Dropped.
class DuplicatesPipeline(object):

    #initializer - set initial values, and, through the RelateIQ API
    #    call all users already present in the Leads list
    def __init__(self):

        self.seen = set() #Items seen in previous scrapes
        self.seenN = set() #Item Names seen in previous scrapes
        self.seenC = set() #Item Company Names seen in previous scrapes

        #Connects to the RelateIQ API w/a Public & Private Key
        RelateIQ("554bd961e4b0957bd04218f3", "75NyjX91ZvyX9hSUrkjSwFCdp3L")
        #Connects to the Leads List (w/specific ListID)
        listObj = List("54f14ea2e4b0c7427aeaa17f")

        #Variables to iterate through pages
        x1 = 0
        x2 = x1 + 150

        #Loops through the pages in the RelateIQ DB
        while True:

            #fetches items between x1 and x2 (0 to 150 initially)
            #    and stores in listItems
            listItems = listObj.ListItems.fetchPage(x1,x2)

            #if the page fetch is returning None
            if not listItems:
                break #break out of the outer while loop

            #iterate through the listItems...a json representation of
            #    the information retrieved through the RelateIQ database
            for x in listItems:
                #iterates through every (key,value) pair
                for key, value in x.fieldValues().iteritems():
                    #looking for ID 58 [email]
                    if (key == u'58'):
                        self.seen.add(value)
                    #looking for ID 51 [companyName]
                    if (key == u'51'):
                        self.seenC.add(value.lower())

                #changes strings to lowercase to simplify comparison
                t = x.name()
                t = t.lower()

                #adds scraped name (lowercased) to self.seenN
                self.seenN.add(t)

            #adds 150 to x1 and x2
            x1 = x2
            x2 = x1 + 150

    #every Item is run through this function at the precise moment it is
    #    scraped from the ProAdvisor databases
    def process_item(self, item, spider):
        #email stores a lowercased version of the scraped email from the
        #    ProAdvisor database [to be used for comparison]
        email = item['email']
        email = email.lower()

        #temporary copies of the name and company name
        tempName = item['firstName'] + " " + item['lastName']
        compName = item['companyName']

        #initializes a boolean variable to check if item has been dropped
        drop = False

        #checks for duplicate email
        if email in self.seen:
            raise DropItem('Duplicate email found %s' % email)
            drop = True

        #checks for duplicate name AND company (if email isn't present)
        if tempName in self.seenN:
            if compName in self.seenC:
                raise DropItem('Duplicate NAME OR EMAIL found %s, %s', tempName, compName)
                drop = True

        #variable to determine if person uses QBO or QBD. Defaults to QBO.
        abc = "0"

        #checks item if uses QBO
        if item['qbo'] == "FALSE":
            abc = "1"

        #if item isn't dropped the following is used to add scraped information
        #    to RelateIQ as Contact, then Contact is added to the Leads list
        #    with certain field values
        if not drop:

            #contact created with certain attributes
            contact = Contact()
            contact.name(string.capwords(tempName)) #name attribute
            contact.email(email) #email attribude
            contact.phone([item['phoneNumber']]) #phone number attribute
            contact.company(string.capwords(item['companyName'])) #company attribute
            contact.create() #created

            listObj = List("54f14ea2e4b0c7427aeaa17f") #calls the Leads list
            listItem = ListItem(parent = listObj) #initializes a listItem
            listItem.contactIds([contact.id()]) #links to the contact created
            listItem.name(string.capwords(contact.name())) #adds name
            #updates certain field values based on IDs
            listItem.fieldValues({"61":"2","58":contact.email(),
                "51":contact.company(),"72":"0","87":"1","100":abc})
            listItem.create() #created

        self.seen.add(email) #adds email to self.seen set
        self.seenC.add(compName) #adds companyName to self.seenC set
        self.seenN.add(tempName) #adds name to self.seenN set

        return item #yields item
