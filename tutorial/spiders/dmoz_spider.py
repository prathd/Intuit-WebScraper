#import useful libraries
import scrapy
import json

from tutorial.items import DmozItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule

#initialize class to create the scraper (spider)
class DmozSpider(scrapy.Spider):

    name = "proadvisor" #name the spider
    allowed_domains = ["proadvisorservice.intuit.com"] #set domain to scrape

    min_lat = 30
    max_lat = 31
    min_long = -100
    max_long = -99

    haw_min_long = 0
    haw_max_long = 0
    haw_min_lat = 0
    haw_max_lat = 0

    alas_min_long = 0
    alas_max_long = 0
    alas_min_lat = 0
    alas_max_lat = 0

    #all longitudes and latitudes covered in Mainland America
    #min_lat = 24
    #max_lat = 50
    #min_long = -125
    #max_long = -65

    #all longitudes and latitudes covered in Hawaii
    #haw_min_long = -175
    #haw_max_long = -153
    #haw_min_lat = 20
    #haw_max_lat = 30

    #all longitudes and latitudes covered in Alaska
    #alas_min_long = -170
    #alas_max_long = -140
    #alas_min_lat = 54
    #alas_max_lat = 71

    #start going through the webpages
    def start_requests(self):

        #mainland USA coordinates
        for i in range(self.min_lat, self.max_lat):
            for j in range(self.min_long, self.max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

        #hawaii coordinates
        for i in range(self.haw_min_lat, self.haw_max_lat):
            for j in range(self.haw_min_long, self.haw_max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

        #alaska coordinates
        for i in range(self.alas_min_lat, self.alas_max_lat):
            for j in range(self.alas_min_long, self.alas_max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

    #given the JSON information from the AJAX webpage, this function will
    #    parse through the data. It MUST be present.
    def parse(self, response):
        #load JSON key,value information into jsonresponse
        jsonresponse = json.loads(response.body_as_unicode())

        #loop through the items in searchResults within jsonresponse
        for x in jsonresponse['searchResults']:

            item = DmozItem() #initialize a DmozItem

            #get outlines field values and store them in item
            item['firstName'] = x['firstName'].lower() #First Name
            item['lastName'] = x['lastName'].lower() #Last Name
            item['email'] = x['email'].lower() #E-mail
            item['companyName'] = x['companyName'].lower() #Company Name

            if x.get('phoneNumber'): #Phone Number IF present
                item['phoneNumber'] = x['phoneNumber']
            else: #else store None
                item['phoneNumber'] = None

            o = x['qbopapCertVersions'] #qbo Certification
            d = x['papCertVersions'] #qbd Certification

            #Change to TRUE or FALSE rather than years of Certification
            if not o:
              item['qbo'] = "FALSE"
            else:
              item['qbo'] = "TRUE"

            if not d:
              item['qbd'] = "FALSE"
            else:
              item['qbd'] = "TRUE"

            yield item #output the item
