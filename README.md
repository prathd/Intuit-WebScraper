# ProAdvisor Scraper
Crawls QBO Databases for new leads and updates the RIQ Leads List

In order to RUN spider, call python proadvisor_script.py

    // Will initially scrape the RelateIQ database for all leads currently present (will occur in sets of
    //     ...150 at a time, as there is a limit set by RelateIQ)
    // Crawl the ProAdvisor database for potential leads that are NOT PRESENT in the data scraped from RIQ
    //     ...comparison will be based on E-mail/Name/Company Name
    // All unique individuals found (not already present in RIQ) will be created as contacts in RIQ, and then
    //     ...added to the Leads List within Relate IQ


Important Files:

    1/ tutorial/items.py - Sets categories for all data scraped from ProAdvisor
    2/ tutorial/filter_pipeline.py - Scraped items will go through this filter pipeline
    3/ tutorial/spiders/dmoz_spider.py - The spider that will crawl the database
    4/ proadvisor_script.py - The script that calls your the spider through a CLI
