# First import the required modules,
# xpath_check, mysql_connection & product_scrape_xpaths are custom build 
# modules found in the same folder as the spiders.
import scrapy
from scrapy.exceptions import CloseSpider
from scraper1.items import ScraperProductItem
# from scrapy_splash import SplashRequest
import requests
import urlparse
import urllib
import MySQLdb
import logging
import sys
import xpath_check
import mysql_connection
import product_scrape_xpaths
from datetime import datetime
import time
import pprint
from scrapyd_api import ScrapydAPI
import ProxyService
import re
    
# Create the main class of the spider (object-oriented programming)
class NewProductSpider(scrapy.Spider):
    # Set the short-name for this spider:
    name = "ScrapeNewProduct"
    # This spider is allowed to handle responses with a 404 
    handle_httpstatus_list = [404]
    
    # Set the Pipeline to be used after scraping
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper1.pipelines.pipelines.MySQLStoreProduct': 100                    
        }
    }

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
    def __init__(self, source = 0, test = 0, limit = 0, *args, **kwargs):
        super(NewProductSpider, self).__init__(*args, **kwargs)
        self.source = source
        self.test = test
        self.limit = limit
        # Store the source and date in a report summary variable
        self.report_summary = []
        self.report_summary.append("Source: %s" % source)
        self.report_summary.append("Test: %s" % test)
        self.report_summary.append("Date: %s" % (
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        # Return an error in case no source code was passed along.
        if self.source == 0:
            self.logger.critical("No source code was passed along!")
            sys.exit()

        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
        
        # Get proxies because FP needs an additional request
        # This is needed because of some javascript on the product page.
        # if self.source == 5 or self.source == '5':
            #self.proxy_list = ProxyService.get_proxies()      
    
    
    # Overwrite the default start_request function.
    # In order to be able to pull  (start) URLs from the database,
    # and run them in concurrently.
    def start_requests(self):  
    
        # Now fetch some URLs from the product_urls table.
        # Define which table to use according to Test or Real
        if (self.test == 1) or (self.test == '1'):
            query = ("SELECT `id`, `url` "
                "FROM `product_urls` "
                "WHERE `source` = %s AND `status` = 0 "
                "LIMIT {0} ".format(self.limit)
                )
            self.cursor.execute(query,(self.source,))
        else:
            query = ("SELECT `id`, `url` "
                "FROM `product_urls_SCRAPY` "
                "WHERE `source` = %s AND `status` = 0 "
                "LIMIT {0} ".format(self.limit)
                )
            self.cursor.execute(query,(self.source,))
                
        rows = self.cursor.fetchall()
        
        # First store the dictionary with source xpaths in a variable,
        # as obtained from the customer product_scrape_xpaths module.
        self.xpath_dict = product_scrape_xpaths.get_dict()
        
        
        # Because the duplicate filter whe need to set some sources to no filtering because of the not available page
        sources_no_filtering = ['6', '7', '20', '25', '31', '21']
        if self.source in sources_no_filtering:
            no_filter=True
        else:
            no_filter=False        

        
        # Loop through each of the rows, as row.
        # And initiate a scrape for each of them based on the URL, 
        # also pass along the id of the row from the product_urls table as
        # meta data (for later reference), and handle it through the parse 
        # function.
        
        
        for row in rows:
            # Edit the url with some query parameters, for setting USD or location
            query = self.xpath_dict[self.source]['query_url']
            request_url = row[1] + query
        
            yield scrapy.Request(
                url=request_url, meta={'id': row[0], 'url': row[1]}, 
                callback=self.parse, dont_filter=no_filter)
        
        """
        
        for row in rows:
            yield SplashRequest(
                url=row[1], callback=self.parse,  meta={'id': row[0]},
                    args={
                        'wait': 1
                    }                                
            )
                
        """
    def count_new_products(self):
        if (self.test == 1) or (self.test == '1'):
            query = ("SELECT COUNT(*) "
                "FROM `product_urls` "
                "WHERE `source` = %s AND `status` = 0"
                )
            self.cursor.execute(query, (self.source,))
            result=self.cursor.fetchone()
            self.items_left = result[0]
        
        else:
            query = ("SELECT COUNT(*) "
                "FROM `product_urls_SCRAPY` "
                "WHERE `source` = %s AND `status` = 0"
                )
            self.cursor.execute(query, (self.source,))
            result=self.cursor.fetchone()
            self.items_left = result[0]

        self.logger.info('(Re)Run, there are %s products left', str(self.items_left))
    
    # 'parse' is the default function to handle the requests.
    # In this case as initiated from the start_requests function.
    def parse(self, response):
        
        xpath_dict = self.xpath_dict
        # Define the source from self.source (easier call-name),
        # which is set while calling the spider and passed as an argument,
        # which is we catch using __init__ function (above).
        source = self.source
        # Obtain the product wrapper through xpath, and store it in the 
        # variable 'product'. This sub-part of the html code allows further,
        # more narrowed down subsequent xpath extracts.
        item = ScraperProductItem()
        # Set the product_urls row id based  on meta data passed on to the 
        # callback function.
        
        if response.status == 404 or response.url == xpath_dict[source]['na_url']:
            # Set the source id code (e.g. 4 = banggood).
            item['id'] = response.meta['id']
            item['source'] = source
            # Set the pipeline type; which helps the pipeline handler 
            # to define what to do with the page scrape.
            item['pipeline'] = "SetStatus"
            item['failed'] = False
            # Pass along whether it is a test (0) or 'real' run (1)
            item['test'] = self.test
            
            yield item          
        
        else:
            obtain_product = response.xpath(xpath_dict[source]['product_wrapper'])
            # Check if the extract resulted in anything.
            if obtain_product:
                # Use only the first instance returned from the xpath
                product = obtain_product[0]
                # Initiate the item to store full product information.
                item['id'] = response.meta['id']
                # Set the source id code (e.g. 4 = banggood).
                # Check the database sources table for IDs.
                item['source'] = source
                # Set the pipeline type; which helps the pipeline handler 
                # to define what to do with the page scrape.
                item['pipeline'] = "SetProduct"
                # Set item failed to none, we will use this to drop the item in the
                # pipeline handler on failure.
                item['failed'] = False
                # Pass along whether it is a test (0) or 'real' run (1)
                item['test'] = self.test
                # Original URL to put to hash variant in pipeline
                item['url'] = response.meta['url']
                # Set the Affiliate URL of the product
                
                item['affiliate_link'] = xpath_dict[source]['affiliate_link_before'] + urllib.quote(response.meta['url'].encode('utf-8'), ":, /") + xpath_dict[source]['affiliate_link_after']
                # Set the title of the product, using the custom module xpath_check
                # with the x_string function. Setting empty_error to 1 means that
                # in case the xpath extract returns nothing a critical error is
                # raised and the spider is terminated.
                item['title'] = xpath_check.x_string(
                    wrapper = product,
                    xp = xpath_dict[source]['title'],
                    empty_error = 1)
                    
                        
                        
                # Set the URL / link to the image of the product.
                item['img1'] = xpath_check.x_string(
                                    wrapper = product,
                                    xp = xpath_dict[source]['img_url'],
                                    empty_error = 1)
                                    
                                    
                item['img2'] = xpath_check.x_string(
                                    wrapper = product,
                                    xp = xpath_dict[source]['img_url2'],
                                    empty_error = 0)
                
                item['img3'] = xpath_check.x_string(
                                    wrapper = product,
                                    xp = xpath_dict[source]['img_url3'],
                                    empty_error = 0)

                
                if (item['img1'] is not '') | (item['img1'] is not 'Empty') | (item['img1'] is not None):
                    item['img1'] = urlparse.urljoin('http://', item['img1'])
                    if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.][^\.][\.]*', item['img1']) is None:
                    # OLD REGEX: ^http:\/\/[^\.]+[\.][^\.]+[\.]com[\.]*
                    #if item['img1'] == 'http://' :
                        item['img1'] = 'Empty'
                
                if (item['img2'] is not '') | (item['img2'] is not 'Empty') | (item['img2'] is not None):
                    item['img2'] = urlparse.urljoin('http://', item['img2'])
                    if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.][^\.][\.]*', item['img2']) is None:
                    #if item['img2'] == 'http://' :
                        item['img2'] = ''
                
                if (item['img3'] is not '') | (item['img3'] is not 'Empty') | (item['img3'] is not None):
                    item['img3'] = urlparse.urljoin('http://', item['img3'])
                    if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.][^\.][\.]*', item['img3']) is None:
                    #if item['img3'] == 'http://' :
                        item['img3'] = ''
                
                
                # Set the original / list price of the product, this time using the
                # decimal rather than the string function of the custom
                # xpath_check module (which removes any non-numbers and
                # non-dots from the string -- trying to return a decimal number.
                item['list'] = xpath_check.x_decimal(
                    wrapper = product,
                    xp = xpath_dict[source]['list'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_list'])
                # Set the current (discounted) price of the product.
                item['price'] = xpath_check.x_decimal(
                    wrapper = product,
                    xp = xpath_dict[source]['price'],
                    empty_error = 1)
                # Set the amount of stars this product has, this time allowing
                # for empty returns (which will default to zero).
                item['stars'] = xpath_check.x_decimal(
                    wrapper = product,
                    xp = xpath_dict[source]['stars'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_stars'])
                # Set the count of reviews for this product, allowing empty.
                item['reviews'] = xpath_check.x_decimal(
                    wrapper = product,
                    xp = xpath_dict[source]['reviews'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_reviews'])
                # Set the SKU code of the product.
                item['sku'] = xpath_check.x_string(
                    wrapper = product,
                    xp = xpath_dict[source]['sku'],
                    empty_error = 1)
                # Check if the product is in stock, using the x_stock function
                # od the custom module xpath_check.
                
                # Specific code to extrat the stock value according to a javascript call for Focalprice
                """
                if item['source'] == "5":
                    # Set the needed proxy parameters for the extra request
                    # user_pass = 'eekhoorn:hamsteren'
                    # proxy = 'http://' + user_pass + '@' + ProxyService.select_random_proxy(self.proxy_list)
                    self.logger.info(
                        "Response Meta: %s",
                        response.meta['proxy'])
                    
                    # Call the javascript part
                    url = 'http://dynamic.focalprice.com/QueryStockStatus?sku=%s' % item['sku']
                    r = requests.get(url, proxies=self.proxy_list)
                    data = r.json()
                    
                    # Check the result and set the stock value appropriately
                    if data['allowBuy'] == True:
                        item['stock'] = 0
                    else:
                        item['stock'] = 1
                    self.logger.info(
                    "This is the Request: %s", data['allowBuy'])
                    
                else:
                """
                item['stock'] = xpath_check.x_stock(
                    wrapper = product,
                    xp = xpath_dict[source]['stock'],
                    empty_error = 1,
                    source = source,
                    wildcard = xpath_dict[source]['empty_stock'])
                
                # Set the description of the product, through the x_description
                # function of the custom xpath_check module. And using //text()
                # in the xpath to get all the text values within child nodes.
                # This time not using the 'product' html snippet, but rather the 
                # full page html source code (response) since for banggood
                # product pages the description is outside the main product
                # wrapper-div.
                item['description'] = xpath_check.x_description(
                    wrapper = response,
                    xp = xpath_dict[source]['description'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_description'])
                # Get the source categories     
                item['cat'] = xpath_check.x_string(
                    wrapper = product,
                    xp = xpath_dict[source]['cat'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_cat'])
                item['sub'] = xpath_check.x_string(
                    wrapper = product,
                    xp = xpath_dict[source]['sub'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_sub']) 
                item['subsub'] = xpath_check.x_string(
                    wrapper = product,
                    xp = xpath_dict[source]['subsub'],
                    empty_error = 1,
                    wildcard = xpath_dict[source]['empty_subsub'])                    
                # We've got everything we need for the product. Yield the item, 
                # to let it subsequently be handled by the pipeline handler.
                if 'Empty' in item.values():
                    item['failed'] = True
                    self.logger.critical(
                        "We have an empty item")
            
                yield item    
                  
            else :
                # There was nothing extracted in the product wrapper... Error!
                self.logger.critical(
                    "Main product wrapper xpath (%s) returned empty!",
                    xpath_dict[source]['product_wrapper'])
                sys.exit()

    
    def closed(self, reason):
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
        self.cursor.execute(
            "INSERT INTO `scrapy_logs` "
            "(`spider`, `test`,`log_date`, `log_file`, `stats`, `short_msg`, `long_msg`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('spider_new_products', self.test, time.time(), log_path, stats, s, file_content)
            )
        self.conn.commit()
        # Count the products still need to be done
        self.count_new_products()
        # Close the db connection when done.
        self.conn.close() 
        # Check if we need to rerun the script.
        
        self.logger.info(
            "We still have number of products to update left: %s", self.items_left)
        
        # Force the spider to stop when we cancel the job
        if reason is 'finished':   
            if self.items_left >= 200 and int(self.limit) >= 51: #200
                if (self.test == 1) or (self.test == '1'):
                    scrapyd = ScrapydAPI('http://127.0.0.1:6800')
                    scrapyd.schedule('scraper1', 'ScrapeNewProduct', source=self.source, test='1', limit=self.limit)
                else:
                    self.logger.info ("Don't Reschedule because it's a test run")
            self.logger.info ("Don't Reschedule because limit is smaller then 50 or items is lower than 200")
            

        
           