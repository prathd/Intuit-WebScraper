

class CraigslistSamplePipeline(object):

    def find_row_by_id(item):
        with open('URLlog.txt', 'r') as f:                # open my txt file with urls from previous scrapes
            urlx = [url.strip() for url in f.readlines()] # extract each url
            if urlx == item ["website_url"]:              # compare old url to URL being scraped
            raise DropItem('Item already in db')      # skip record if in url list
        return