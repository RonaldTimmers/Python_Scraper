# First import the required modules,
# xpath_check, mysql_connection & product_scrape_xpaths are custom build 
# modules found in the same folder as the spiders.
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Response 
from scraper1.items import ScraperUpdateItem
import urlparse
import MySQLdb
import logging
import sys
import xpath_check
import mysql_connection
import product_scrape_xpaths
from datetime import datetime
import re # Needed for testing URL's -> TO DO: Maybe better in a higher class
import time
import pprint
from scrapyd_api import ScrapydAPI

# This need to be initiated Somewhere in a Spider to see Results in Console!! 

logging.getLogger().addHandler(logging.StreamHandler())
 
# Create the main class of the spider (object-oriented programming)
class UpdateProductSpider(scrapy.Spider):
    # This spider is allowed to handle responses with a 404 
    handle_httpstatus_list = [404]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper1.pipelines.pipelines.MySQLUpdateProduct': 100                    
        }
    }

    # Set the short-name for this spider:
    name = "ScrapeUpdateProduct"
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
        "zapals.com"
        ]
    
    # Define the initializing function, used to catch the source number
    # passed along while running the spider as an argument (-a).
    def __init__(self, source=0, test=0, limit=0, group=0, cats=0, images=0, descrp=0, *args, **kwargs):
        super(UpdateProductSpider, self).__init__(*args, **kwargs)
        self.source = source
        self.test = test
        self.limit  = limit
        self.updateCategories = cats
        self.updateDescriptions = descrp
        self.updateImages = images
        self.group = group
        
        
        
        # Set the right database Tabels according to if we are Real or Testing
        if (self.test == 1) or (self.test == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (self.test == 0) or (self.test == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'  
            
            
        # Store the source and date in a report summary variable
        self.report_summary = []
        self.report_summary.append("Source: %s" % source)
        self.report_summary.append("Date: %s" % (
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Return an error in case no source code was passed along.
        if self.source == 0:
            logging.critical("No source code was passed along!")
            sys.exit()
              
        
    # Overwrite the default start_request function.
    # In order to be able to pull  (start) URLs from the database,
    # and run them in concurrently.
    def start_requests(self):
        
        # Products are divided in different Groups 
        # Stock, Not in Stock and Not Active (urls.status= = 4)
        

        
        # In Stock
        if (self.group == 0 or self.group == '0'):
            stock = 0 # 0 is in stock
            status = 1
            self.updatetime = time.time() - 172800  # seconds/48 Hours
        
        # Out Stock
        if (self.group == 1 or self.group == '1'):
            stock = 1
            status = 1
            self.updatetime = time.time() - 604800  # seconds/7 days
        
        # Not Active
        if (self.group == 2 or self.group == '2'):
            status = 4
            self.updatetime = time.time() - 2592000  # seconds/30 days

        # For Faster Update Sequence
        if (self.group == 9 or self.group == '9'):
            stock = 0 # 0 is in stock
            status = 1
            self.updatetime = time.time() - 7200  # seconds/48 Hours
    
    
        # Overwrite to 1 second for test purposes 
        if (self.test == 0) or (self.test == '0'):
            self.updatetime = time.time() - 1  # 1 second!
        
        
        # Starting the DB connection
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
        
        
        if (self.updateImages == 1 or self.updateImages == '1'):
            # Different Query If we want to scrape New Images
            # DELETE LATER IMG_STATUS != 9
            query = ("SELECT urls.id, urls.url, urls.url_hash, urls.pid "
                    "FROM `{0}` As urls "
                    "INNER JOIN `{1}` As details "
                    "ON urls.pid = details.id "
                    "WHERE urls.processing = 0 AND urls.source = %s AND urls.status = 1 AND urls.img_status != 9  AND (details.thumbs_extra = 0 OR details.thumbs_extra = 1) "
                    "LIMIT {2}".format(self.urls_table, self.details_table, self.limit) 
            )  
            
            logging.debug(
                "We got the Image Query")
                
            self.cursor.execute(
                query, (self.source, )
            )
        
        # The normal query for Active Products
        elif (self.group == '0' or self.group == '1'):
            # For Clean purposes also take `updated` IS NULL with the query.
            query = ("SELECT urls.id, urls.url, urls.url_hash, urls.pid "
                        "FROM `{0}` As urls "
                        "INNER JOIN `{1}` As details "
                        "ON urls.pid = details.id "
                        "WHERE urls.processing = 0 AND urls.source = %s AND urls.status = %s AND details.stock = %s AND (details.updated < {2} OR details.updated IS NULL) "
                        "ORDER BY details.stock "
                        "LIMIT {3} ".format(self.urls_table, self.details_table, self.updatetime, self.limit) 
            )
            
            self.cursor.execute(
                query, (self.source, status, stock,)
            )
           
        # The  query for Not-Active Products
        # NEED TO BE UPDATED DNRY!
        else:
            # For Clean purposes also take `updated` IS NULL with the query.
            query = ("SELECT urls.id, urls.url, urls.url_hash, urls.pid "
                        "FROM `{0}` As urls "
                        "INNER JOIN `{1}` As details "
                        "ON urls.pid = details.id "
                        "WHERE urls.processing = 0 AND urls.source = %s AND urls.status = %s AND (details.updated < {2} OR details.updated IS NULL) "
                        "ORDER BY details.stock "
                        "LIMIT {3} ".format(self.urls_table, self.details_table, self.updatetime, self.limit) 
            )
            
            self.cursor.execute(
                query, (self.source, status,)
            )
        
            
        rows = self.cursor.fetchall()
        
        if rows:
            # Get a list of selected ID's 
            # Because the processing boolean we are able to use multiple Spiders at once.
            # Update these ID's in the urls table and SET processing to 1 
            id_list = []
            
            for row in rows:
                id_list.append(row[0])
            
            logging.debug(
                "What is the id_list: %s", id_list)
                
            string_id_list = ','.join(map(str, id_list)) 
            self.id_list = string_id_list
           
            query = ("UPDATE `{0}` As urls "
                    "SET urls.processing = 1 "
                    "WHERE urls.source = %s AND urls.id IN ( {1} ) ".format(self.urls_table, string_id_list)         
            )
            
            self.cursor.execute(
                query, (self.source,)
            )
            
            self.conn.commit()
       

        # Close the db connection when done.
        self.conn.close()  
        
        # Get the dict per source with the xpaths
        self.xpath_dict = product_scrape_xpaths.get_dict()
        
        
        # Because the duplicate filter whe need to set some sources to no filtering because of the not available page
        sources_no_filtering = ['6', '7', '20', '22', '25', '28', '30', '31'] # 08-11-2016 - Added GearBest 28 - 27-7-2017 Added TVC 30
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
            
            
            # 11-08-16 Changed dont_redirect to False. Because of 301 and 302 not allowed issues
            if re.match('^http[s]?:\/\/www[\.][^\.]+[\.]com[\.]*', row[1]) is not None:
                yield scrapy.Request(
                    url=request_url, meta={'id': row[0], 'url_hash': row[2], 'pid': row[3], 'dont_redirect': False}, 
                    callback=self.parse, dont_filter=no_filter)
            else:
                logging.warning('Request Error on ID: %s for url %s', row[0], request_url)
                continue
                
                
                
    # 'parse' is the default function to handle the requests.
    # In this case as initiated from the start_requests function.
    def parse(self, response):
        # First store the dictionary with source xpaths in a variable,
        # as obtained from the customer product_scrape_xpaths module.
        xpath_dict = self.xpath_dict
        # Define the source from self.source (easier call-name),
        # which is set while calling the spider and passed as an argument,
        # which is we catch using __init__ function (above).
        source = self.source
        # Initiate the item to store full product information.
        item = ScraperUpdateItem()
        
        # Set the URL of the product
        # item['link'] = response.url NOT NECESSARY
        
        
        # Specific for GearBest - Test if the URL is equal to a normal Product URL
        checkURL =  bool(re.search('^.+pp_[0-9]+.\.html$', response.url))
        
     
        
        
        logging.debug(
            "Check if product page exist: %s",
            checkURL)
        
        # Because Provlems with LITB (25) we added 'main_page=no_found' in response.url
        # Because Provlems with FASTTECH (22) we added 'listing-removed' in response.url
        # NEED A FUTURE PROOF SOLUTION FOR THIS - TEST URLS AGAINST REGEX INSTEAD OF EXACT MATCH URL
        
        if response.status == 404 or response.url == xpath_dict[source]['na_url'] or 'main_page=no_found' in response.url or 'listing-removed' in response.url or ((self.source == 28 or self.source == '28')  and checkURL == False):
            item['id'] = response.meta['id']  
            item['pid'] = response.meta['pid']
            # Set the source id code (e.g. 4 = banggood).
            # Check the database sources table for IDs.
            item['source'] = source
            # Set the pipeline type; which helps the pipeline handler 
            # to define what to do with the page scrape.
            item['pipeline'] = "UpdateStatus"
            item['failed'] = False
            # Pass along whether it is a test (0) or 'real' run (1)
            item['test'] = self.test
            # Set the URL_Hash
            item['url_hash'] = response.meta['url_hash']
            
            yield item
            
        else:
            # Obtain the product wrapper through xpath, and store it in the 
            # variable 'product'. This sub-part of the html code allows further,
            # more narrowed down subsequent xpath extracts.
            obtain_product = response.xpath(xpath_dict[source]['product_wrapper'])
            # Check if the extract resulted in anything.
            if obtain_product:
                
                # BASIC DATA NEEDED 
                
                # Use only the first instance returned from the xpath
                product = obtain_product[0]
                # Set the product_urls row id based  on meta data passed on to the 
                # callback function.
                item['id'] = response.meta['id']
                item['pid'] = response.meta['pid']
                # Set the source id code (e.g. 4 = banggood).
                # Check the database sources table for IDs.
                item['source'] = source
                # Set the pipeline type; which helps the pipeline handler 
                # to define what to do with the page scrape.
                item['pipeline'] = "UpdateProduct"
                # Set item failed to none, we will use this to drop the item in the
                # pipeline handler on failure.
                item['failed'] = False
                # Pass along whether it is a test (0) or 'real' run (1)
                item['test'] = self.test
                # Set the URL_Hash
                item['url_hash'] = response.meta['url_hash']
                # Set the original / list price of the product, this time using the
                # decimal rather than the string function of the custom
                # xpath_check module (which removes any non-numbers and
                # non-dots from the string -- trying to return a decimal number.
                
                
                # MAIN UPDATE DATA 
                                
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
                # Check if the product is in stock, using the x_stock function
                # od the custom module xpath_check.
                item['stock'] = xpath_check.x_stock(
                    wrapper = product,
                    xp = xpath_dict[source]['stock'],
                    empty_error = 1,
                    source = source,
                    wildcard = xpath_dict[source]['empty_stock'])
                  
                
                # EXTRA UPDATE CATEGORY 
                
                if (self.updateCategories == 1 or self.updateCategories == '1'):
                    # Get the source categories     
                    item['cat'] = xpath_check.x_string(
                        wrapper = product,
                        xp = xpath_dict[source]['cat'],
                        empty_error = 1)
                    item['sub'] = xpath_check.x_string(
                        wrapper = product,
                        xp = xpath_dict[source]['sub'],
                        empty_error = 1) 
                    item['subsub'] = xpath_check.x_string(
                        wrapper = product,
                        xp = xpath_dict[source]['subsub'],
                        empty_error = 1,
                        wildcard = xpath_dict[source]['empty_subsub']) 

                # EXTRA UPDATE DESCRIPTIONS
                
                if ( self.updateDescriptions == 1 or self.updateDescriptions == '1' ):
                    item['description'] = xpath_check.x_description(
                                            wrapper = response,
                                            xp = xpath_dict[source]['description'],
                                            empty_error = 1,
                                            wildcard = xpath_dict[source]['empty_description'])     
                                            
                        
                # EXTRA UPDATE IMAGES 
                            
                if (self.updateImages == 1 or self.updateImages == '1'):
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
                        if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.]com[\.]*', item['img1']) is None:
                        #if item['img1'] == 'http://' :
                            item['img1'] = 'Empty'
                    
                    if (item['img2'] is not '') | (item['img2'] is not 'Empty') | (item['img2'] is not None):
                        item['img2'] = urlparse.urljoin('http://', item['img2'])
                        if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.]com[\.]*', item['img2']) is None:
                        #if item['img2'] == 'http://' :
                            item['img2'] = ''
                    
                    if (item['img3'] is not '') | (item['img3'] is not 'Empty') | (item['img3'] is not None):
                        item['img3'] = urlparse.urljoin('http://', item['img3'])
                        if re.match('^http[s]?:\/\/[^\.]+[\.][^\.]+[\.]com[\.]*', item['img3']) is None:
                        #if item['img3'] == 'http://' :
                            item['img3'] = ''

                        
                    
                # We've got everything we need for the product. Yield the item, 
                # to let it subsequently be handled by the pipeline handler.
                if 'Empty' in item.values():
                    item['failed'] = True
                    self.logger.critical(
                        "We have an empty item")            
                
                yield item
      
            else:
                # There was nothing extracted in the product wrapper... Error!
                logging.critical(
                    "Main product wrapper xpath (%s) returned empty!",
                    xpath_dict[source]['product_wrapper'])
                sys.exit()
            
    def count_products_update(self):
        # Starting the DB connection
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
        
        if (self.updateImages == 1 or self.updateImages == '1'):
            # Different Query If we want to scrape New Images
            # DELETE LATER IMG_STATUS != 9
            query = ("SELECT COUNT(*) "
                    "FROM `{0}` As urls "
                    "INNER JOIN `{1}` As details "
                    "ON urls.pid = details.id "
                    "WHERE urls.source = %s AND urls.status = 1 AND urls.img_status != 9 AND details.thumbs_extra = 0 AND details.active = 1 AND details.stock = 0 "
                    "LIMIT {2}".format(self.urls_table, self.details_table, self.limit) 
            ) 
        

        if (self.group == 0 or self.group == '0'):
            query = ("SELECT COUNT(*) "
                    "FROM `{0}` As urls "
                    "INNER JOIN {1} As details "
                    "ON urls.pid = details.id "
                    "WHERE urls.source = %s AND urls.status = 1 AND details.stock = 0 AND (details.updated < {2} OR details.updated IS NULL) "
                    "LIMIT {3}".format(self.urls_table, self.details_table, self.updatetime, self.limit) 
            )
            
        if (self.group == 1 or self.group == '1'):
            query = ("SELECT COUNT(*) "
                    "FROM `{0}` As urls "
                    "INNER JOIN {1} As details "
                    "ON urls.pid = details.id "
                    "WHERE urls.source = %s AND urls.status = 1 AND details.stock = 1 AND (details.updated < {2} OR details.updated IS NULL) "
                    "LIMIT {3}".format(self.urls_table, self.details_table, self.updatetime, self.limit) 
            )
            
        if (self.group == 2 or self.group == '2'):
            query = ("SELECT COUNT(*) "
                    "FROM `{0}` As urls "
                    "INNER JOIN {1} As details "
                    "ON urls.pid = details.id "
                    "WHERE urls.source = %s AND urls.status = 4 AND (details.updated < {2} OR details.updated IS NULL) "
                    "LIMIT {3}".format(self.urls_table, self.details_table, self.updatetime, self.limit) 
            )
        
        
        
        
        self.cursor.execute(query, (self.source,))
        result = self.cursor.fetchone()
        
        # Close the db connection when done.
        self.conn.close()
        
        self.items_left = result[0]

        self.logger.info('(Re)Run, there are %s products left', str(self.items_left))
        
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
        
        # Starting the DB connection
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
        
        
        # Because Sometimes the proccessing status will not reset back 
        # Check all Id's in the initial list and reset them to 0 for not processing
        try:
            self.id_list
        except (NameError, AttributeError):
            print "well, it WASN'T defined after all!"
        else:
            print "sure, it was defined."
            self.logger.info(
                "self.id_list: %s", self.id_list)
                
            query = ("UPDATE `{0}` as urls "
                    "SET urls.processing = 0 "
                    "WHERE urls.processing = 1 AND urls.id IN ( {1} ) ".format(self.urls_table, self.id_list)
                    )

            self.cursor.execute(query)
            
            self.logger.info(
                "We Cleared the items which were still processing")
            

        self.cursor.execute(
            "INSERT INTO `scrapy_logs` "
            "(`spider`, `test`, `log_date`, `log_file`, `stats`, `short_msg`, `long_msg`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('spider_update_products', self.test, time.time(), log_path, stats, s, file_content)
            )
            
        self.conn.commit()
        
        # Close the db connection when done.
        self.conn.close()   
        
        # Count the number of products to be updated left
        self.count_products_update()
        
       

        self.logger.info(
            "We still have number of products to update left: %s", self.items_left)
        
        # Force the spider to stop when we cancel the job
        if reason is 'finished':
            if self.items_left >= 1000 and int(self.limit) >= 499:
                if (self.test == 1) or (self.test == '1'):
                    scrapyd = ScrapydAPI('http://127.0.0.1:6800')
                    scrapyd.schedule('scraper1', 'ScrapeUpdateProduct', source=self.source, test='1', limit=self.limit, cats=self.updateCategories, descrp=self.updateDescriptions, images=self.updateImages, group=self.group)
                else:
                    self.logger.info ("Don't Reschedule because it's a test run")
            else:
                self.logger.info ("Don't Reschedule because limit is smaller then 1001 or items is lower than 1000")
            