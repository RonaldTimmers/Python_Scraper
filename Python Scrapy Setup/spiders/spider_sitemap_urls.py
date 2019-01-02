# First import the required modules,
# xpath_check and product_scrape_xpaths are custom build modules,
# found in the same folder as the spiders.
import scrapy
from scrapy.exceptions import CloseSpider
from scraper1.items import ScraperURLItem
import urlparse
import logging
import xpath_check
import mysql_connection
import product_scrape_xpaths
from datetime import datetime
import time
import sys
import pprint
import random

    
# Create the main class of the spider (object-oriented programming)
class NewSitemapSpider(scrapy.Spider):
    # Set the Pipeline to be used after scraping
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper1.pipelines.pipelines.MySQLStoreURL': 100    
        },
        'CLOSESPIDER_ITEMCOUNT': 200000
    }

    # Set the short-name for this spider:
    name = "ScrapeSitemapURLs"
    # Restrict the domain name which the spider can operate on.
    # Make sure to append the list for new sources.
    allowed_domains = [
        "dx.com",
        "banggood.com",
        "focalprice.com",
        "miniinthebox.com",
        "lightinthebox.com",
        "tmart.com",
        "gearbest.com",
        "tinydeal.com",
        "geekbuying.com",
        "dealsmachine.com",
        "newfrog.com",
        "tomtop.com",
        "fasttech.com",
        "chinavasion.com",
        "tvc-mall.com",
        "antelife.com",
        "cafago.com",
        "chinabuye.com",
        "dinodirect.com", 
        "sunsky-online.com",
        "cndirect.com",
        "zapals.com",
        "shein.com", 
        "camfere.com",
        "rcmoment.com",
        "romwe.com",
        "newchic.com",
        "rotita.com"
        ]
      

    # Define the initializing function, used to catch the source number
    # passed along while running the spider as an argument (-a).
    def __init__(self, source = 0, test = 0, *args, **kwargs):
        super(NewSitemapSpider, self).__init__(*args, **kwargs)    
        self.source = source
        self.test = test
        
        # Store the source and date in a report summary variable
        self.report_summary = []
        self.report_summary.append("Source: %s" % source)
        self.report_summary.append("Test: %s" % test)
        self.report_summary.append("Date: %s" % (
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        # Create a page counter variable
        self.page_counter = 1
        # Create a product counter variable
        self.product_counter = 0
        # Return an error in case no source code was passed along.
        if self.source == 0:
            self.logger.critical("No source code was passed along!")
            #sys.exit()
            raise CloseSpider('No source.')
        # Set the xpath dictionary.
        # Which stores all the information per source in the custom
        # module called product_scrape_xpaths.
        self.xpath_dict = product_scrape_xpaths.get_dict()

    # Overwrite the default start_request function.
    # In order to be able to pull  (start) URLs from the xpath dict.
    def start_requests(self):
        self.logger.critical("DEPTH_LIMIT: %s", self.settings['DEPTH_LIMIT'])
        # Now loop through the urls / links listed in start_urls in
        # the xpath dictionary as set in the __init__ and start
        # scraping.
        yield scrapy.Request( url=self.xpath_dict[self.source]['sitemap_url'], 
                        callback=self.parseURLs)

    def parseURLs(self, response):
        # First store the dictionary with source xpaths in a variable,
        # as obtained and set during the __init__ but store it under
        # shorter / easier call-name.
        xpath_dict = self.xpath_dict
        
        # Define the source from self.source (easier call-name),
        # which is set while calling the spider and passed as an argument,
        # which is we catch using __init__ function (above).
        source = self.source    
        
        # Get start url of source
        start_url =  "".join(xpath_dict[source]['start_urls'])
        
        # If the Sitemap consist out of multiple pages. 
        # Select the next sitemap page for later on.
        # Sources: Chinabuye - 10
        if self.source in ['10']:
            self.nextpage_sitemap = "".join(response.xpath(xpath_dict[source]['next_page']).extract())
            
            self.logger.info(
                "We got a Next Sitemap: %s", self.nextpage_sitemap)
        
        else:
            self.nextpage_sitemap = None
        
        # Check if there are links in the sitemap 
        if response.xpath(xpath_dict[source]['sitemap_link']) is not None:
        
            # wrapper.xpath(xp).extract()
            category_links = response.xpath(xpath_dict[source]['sitemap_link']).extract()
            
            # Randomize the URL's in order to not start at the same place when restarting spider
            random.shuffle(category_links)
            
            for category_link in category_links:
                # Create the correct url
                url = urlparse.urljoin(
                    start_url,
                    category_link)
                
                self.logger.info(
                    "Category_link: %s", url)
                      
                yield scrapy.Request(url=url, callback=self.parse)
                
            
            
            
            
    # 'parse' is the default function to handle the requests 
    # in this spider, the start_urls entries are downloaded
    # and handled through this function to start with.
    def parse(self, response):
   
        
        # First store the dictionary with source xpaths in a variable,
        # as obtained and set during the __init__ but store it under
        # shorter / easier call-name.
        xpath_dict = self.xpath_dict
        # Define the source from self.source (easier call-name),
        # which is set while calling the spider and passed as an argument,
        # which is we catch using __init__ function (above).
        source = self.source
        # either get main source url
        source_url = xpath_dict[source]['source_url']
        # Loop through all the product listings, using the xpath of 
        # the wrapper. Catch each extract in the variable 'product'.
        for product in response.xpath(xpath_dict[source]['product_list_item']):
            # For each product initiate an URL scrape item.
            item = ScraperURLItem()
            # Set the source id, e.g. Banggood = 4.
            item['source'] = source
            # Set the pipeline type; which helps the pipeline handler 
            # to define what to do with the page scrape.
            item['pipeline'] = "NewUrl"
            # Set item failed to none, we will use this to drop the item in the
            # pipeline handler on failure.
            item['failed'] = False
            # Extract the product title using the xpath within the previously
            # extracted wrapper xpath, and check the extract for a valid
            # outcome (e.g. not empty) using the custom x_string function from
            # the xpath_check module. The '1' passed along to the x_string
            # function tells it to throw an error in case the extract failed /
            # no item with that xpath is found.
            item['title'] = xpath_check.x_string(
                wrapper = product,
                xp = xpath_dict[source]['product_list_title'],
                empty_error = 1)
            # Extract the URL of the product and validate
            item['url'] = urlparse.urljoin(source_url, (urlparse.urlparse(xpath_check.x_string(
                wrapper = product,
                xp = xpath_dict[source]['product_list_url'],
                empty_error = 1)).path))
            # Pass along whether it is a test (0) or 'real' run (1)
            item['test'] = self.test
            # increase the product counter by 1
            self.product_counter += 1
            # Now we have everything we need, yield the item.
            # i.e. pass it to the pipeline handler
            if 'Empty' in item.values():
                item['failed'] = True
                self.logger.critical(
                    "We have an empty item")
                    
            yield item

        # Get start url of source
        # Convert List result into String
        start_url =  "".join(xpath_dict[source]['start_urls'])   
        
        # Extract the link to the next page of new-arrivals,
        # as long as it exists
        # and Convert List result into String
        # log the next page
        """
        xpath_result = response.xpath(xpath_dict[source]['next_page'])
        self.logger.info(
            "xpath_dict[source]['next_page']: %s ", 
            xpath_result)
        """
        
        if response.xpath(xpath_dict[source]['next_page']) is not None:
            next_page =  "".join(
                response.xpath(xpath_dict[source]['next_page']).extract())

            # Check if a next page exists, and if so....
            if next_page:
                self.logger.info(
                    "Response.url : %s", response.url)
            
            
                self.logger.info(
                    "Next Page URL: %s", next_page)
                    
                # Extract the (first) URL to the next page, and log it.
                # Create the correct url
                Nexturl = urlparse.urljoin(
                    response.url,
                    next_page) 
                
                # log the next page
                self.logger.info(
                    "Next page found: %s - initiating new scrape.",
                    Nexturl)
                    
                # Now run the scrape through this function (parse) again 
                # for this 'next page' again. Thereby initiating a loop until
                # there is no longer a 'next page' available.
                yield scrapy.Request(url=Nexturl, callback=self.parse)
                         
        if self.nextpage_sitemap is not None:
            self.logger.info(
                "Next sitemap found: %s - initiating new scrape.",
                self.nextpage_sitemap)
                
            yield scrapy.Request(url=self.nextpage_sitemap, callback=self.parseURLs)
    
    def closed(self, reason):
        #add the number of pages scraped to the summary
        self.report_summary.append("# Pages scraped: %d" % self.page_counter)
        #add the number of products scraped to the summary
        self.report_summary.append("# Products scraped: %d" % (
            self.product_counter))
        # join all the report summary strings together, 
        # with a new line '\n' in between
        stats = self.crawler.stats.get_stats()
        stats = pprint.pformat(stats)
        s = '\n'.join(self.report_summary)
        # log the summary report as stored in 's'
        self.logger.info(s)
    
        # Store the log to our mysql db if it's not a test run
        # Open the log file and retrieve its content
        log_path = self.settings.get('LOG_FILE')
        file = open(
            '%s' % log_path, 
            'r')
        file_content = file.read()
        file.close()
        # Store the log to our mysql db
        # Start the db connection through the custom module.
        conn = mysql_connection.setup_conn()
        # Now fetch some URLs from the product_urls table.
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO `scrapy_logs` "
            "(`spider`, `test`,`log_date`, `log_file`, `stats`, `short_msg`, `long_msg`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('spider_new_urls', self.test, time.time(), log_path, stats, s, file_content)
            )
        conn.commit()
        # Close the db connection when done.
        conn.close()