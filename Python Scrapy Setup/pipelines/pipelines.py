# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# First import the packages and modules required for this program.
# mysql_adbapi_connection is custom build and the file can be found
# in the same folder as the pipelines.py file.
from twisted.enterprise import adbapi
import MySQLdb.cursors
import logging
import mysql_adbapi_connection
import time
from scrapy.pipelines.images import ImagesPipeline                  # Added!!!
from scrapy.exceptions import DropItem                                   # Added!!!
from scrapy.http import Request                                              # Added!!!
import sys


"""
There are 3 main pipelines:

MySQLStoreURL
This Pipeline stores the new scraped product urls from the spiders 
SpiderNewURLs and SpiderSitemap

MySQLStoreProduct
This Pipeline stores the new scraped product data 
SpiderNewProduct

MySQLUpdateProduct
This Pipeline stores the updated product data
SpiderUpdateProduct

"""

class MySQLStoreURL(object):

    
    def open_spider(self, spider): 
        # Function which runs when the pipeline is initiated, which sets up the
        # MySQL connection through adbapi.
        # set db pool by using the custom build mysql_adbapi_connection module.
        if hasattr(spider, 'eu'): 
            self.eu_spider = True
            self.dbpool = mysql_adbapi_connection.setup_eu_conn_adbapi()
        else:
            self.eu_spider = False
            self.dbpool = mysql_adbapi_connection.setup_conn_adbapi()
    
        logging.basicConfig(
            filemode='w', level=logging.INFO)  
            
        log_path = spider.settings.get('LOG_FILE')

        open(
            '%s' % log_path, 
            'w')

        logging.info(
            "We are running this spider: %s",
            spider.name)
    
    def close_spider(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()        
 
    # The function which actually handles the spider item yields:
    def process_item(self, item, spider):
        if item['failed']:
            raise DropItem("We have an failed item")
        else:            
            # Run db query in thread pool to process the new list of prod URLs.
            # Use the _conditional_insert function of this class (below),
            # and feed it the item as passed along by the spider.
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            
            return item
 
    def _conditional_insert(self, tx, item):
        # Check if the product doesn't already exist in the product_urls table.
        if (item['test'] == 0) or (item['test'] == '0'):        
            tx.execute(
                "SELECT `id` FROM `product_urls_SCRAPY` "
                "WHERE `url_hash` = MD5(%s) AND `url` = %s",
                (item['url'], item['url']))
        
        elif (item['test'] == 1) or (item['test'] == '1'):        
            tx.execute(
                "SELECT `id` FROM `product_urls` "
                "WHERE `url_hash` = MD5(%s) AND `url` = %s",
                (item['url'], item['url']))
        
        result = tx.fetchone()
            
        if result:
            # Already there, don't process to prevent duplicates.
            logging.info("Item already stored in db: %s", item['url'])
        else:
            # Not yet in the product_urls table, store it as a new record
            # First check if this is a test run (0) or a real run (1)
            if (item['test'] == 0) or (item['test'] == '0'):
                # Don't execute DB query since it is only a test run
                logging.info("Item stored in TEST TABLE since it is only a test run: %s", item['url'])
                
                
                """
                7-25-17 
                Update in the Future product_urls tables with url_query 
                NOW only available for EU scraper and in EU database
                
                """
                
                if self.eu_spider:
                    tx.execute(
                        "INSERT INTO `product_urls_SCRAPY` (`source`,`url_hash`,`url`, `url_query`) "
                        "VALUES (%s, MD5(%s), %s, %s)",
                        (item['source'], item['url'], item['url'], item['url_query'])
                        )
      
                else:
                    tx.execute(
                        "INSERT INTO `product_urls_SCRAPY` (`source`,`url_hash`,`url`) "
                        "VALUES (%s, MD5(%s), %s)",
                        (item['source'], item['url'], item['url'])
                        )
                    
            elif (item['test'] == 1) or (item['test'] == '1'):
                
                if self.eu_spider:
                    tx.execute(
                        "INSERT INTO `product_urls` (`source`,`url_hash`,`url`, `url_query`) "
                        "VALUES (%s, MD5(%s), %s, %s)",
                        (item['source'], item['url'], item['url'], item['url_query'])
                        )                    
                else:
                    tx.execute(
                        "INSERT INTO `product_urls` (`source`,`url_hash`,`url`) "
                        "VALUES (%s, MD5(%s), %s)",
                        (item['source'], item['url'], item['url'])
                        )
                        
                logging.info("Item stored in db: %s", item['url'])
            else:
                logging.critical("Invalid Test Value")

    def handle_error(self, e):
        logging.error(e)
     
class MySQLStoreProduct(object):

    def open_spider(self, spider): 
        # Function which runs when the pipeline is initiated, which sets up the
        # MySQL connection through adbapi.
        # set db pool by using the custom build mysql_adbapi_connection module.
        if hasattr(spider, 'eu'): 
            self.dbpool = mysql_adbapi_connection.setup_eu_conn_adbapi()
        else:
            self.dbpool = mysql_adbapi_connection.setup_conn_adbapi()
    
    
        logging.basicConfig(
            filemode='w', level=logging.INFO)  
            
        log_path = spider.settings.get('LOG_FILE')

        open(
            '%s' % log_path, 
            'w')

        logging.info(
            "We are running this spider: %s",
            spider.name)
            
    def close_spider(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()        
 
    # The function which actually handles the spider item yields:
    def process_item(self, item, spider):
            # Run db query in thread pool to process the fully scraped product.
            # Use the _conditional_new_sku function of this class (below),
            # and feed it the item as passed along by the spider.
            if item['failed']:
                raise DropItem("We have an failed item %s", item['id'])
            else:      
                if item['pipeline'] is 'SetStatus':
                    query = self.dbpool.runInteraction(self._conditional_update_url, item)
                    query.addErrback(self.handle_error) 
                elif item['pipeline'] is 'SetProduct':
                    query = self.dbpool.runInteraction(self._conditional_new_sku, item)
                    query.addErrback(self.handle_error) 

                return item
    
    def _conditional_update_url(self, tx, item):    
        logging.info(
            "Because of 404 response, update status to 4 in product_urls with id: %s",
            item['id'])
            
   
        # First check if this is a test run (0) or a real run (1)
        if (item['test'] == 0) or (item['test'] == '0'):
             # Don't execute DB query since it is only a test run
            logging.debug("Item NOT(!) stored in real db since it is only a test run: %s", item['id'])       
            tx.execute(
                "UPDATE `product_urls_SCRAPY` SET `status`= 4  WHERE `id` = %s",
                (item['id'],)
                )
        
        elif (item['test'] == 1) or (item['test'] == '1'):
            tx.execute(
                "UPDATE `product_urls` SET `status`= 4  WHERE `id` = %s",
                (item['id'],)
                )
        

        logging.info(
            "Item set to status = 4 in product_urls: %s", 
            item['id']
            )         
            
    def _conditional_new_sku(self, tx, item):
  
        logging.info(
            "Processing item from product_urls with id: %s",
            item['id'])
        
        # First update the SKU code and the IMG path in the product_urls table.
        
        ######## ADDED MULTIPLE IMAGE PATHS ###########
        if (item['test'] == 1) or (item['test'] == '1'):
            tx.execute(
                "UPDATE `product_urls` SET `sku` = %s, `img` = %s, `img2` = %s, `img3` = %s WHERE `id` = %s",
                (item['sku'],item['img1'],item['img2'],item['img3'],item['id'])                
                )
        else:
            tx.execute(
                "UPDATE `product_urls_SCRAPY` SET `sku` = %s,  `img` = %s, `img2` = %s, `img3` = %s WHERE `id` = %s",
                (item['sku'],item['img1'],item['img2'],item['img3'],item['id'])                
                )            
            
        # Now check for duplicates in the product_urls table based on the 
        # SKU code
        if (item['test'] == 1) or (item['test'] == '1'):
            tx.execute(
                "SELECT `id` FROM `product_urls` WHERE `source` = %s AND `sku` = %s AND `id` <> %s",
                (item['source'],item['sku'],item['id'],)
                )
        else:
            tx.execute(
                "SELECT `id` FROM `product_urls_SCRAPY` WHERE `source` = %s AND `sku` = %s AND `id` <> %s",
                (item['source'],item['sku'],item['id'],)
                )            
        
        result = tx.fetchone()
        if result:
            # Duplicate found! Set status to 2 (duplicate record).
            logging.info(
                "Item %s already stored in db in product_urls table, update status (2)",
                item['url']
                )
            
            if (item['test'] == 1) or (item['test'] == '1'):
                tx.execute(
                    "UPDATE `product_urls` SET `status` = 2 WHERE `id` = %s",
                    (item['id'],)
                    )
            else: 
                tx.execute(
                    "UPDATE `product_urls_SCRAPY` SET `status` = 2 WHERE `id` = %s",
                    (item['id'],)
                    )                
            
        else:
            # No duplicate on SKU code, now check if this product already 
            # exists in the product_details_SCRAPY table.
            logging.debug(
                "Checking the url_hash from %s", (item['url'])
                )            
            
            if (item['test'] == 1) or (item['test'] == '1'):
                tx.execute(
                    "SELECT `id` FROM `product_details` "
                    "WHERE `url_hash` = MD5(%s) ",
                    [item['url']]
                    )
            else:
                tx.execute(
                    "SELECT `id` FROM `product_details_SCRAPY` "
                    "WHERE `url_hash` = MD5(%s) ",
                    [item['url']]
                    )            
                
            row = tx.fetchone()

                
            if row:
                logging.debug("Oke, we got an hit the this product already exist in details with id: %s", (row['id'])
                    )
                # Product already in product_details_SCRAPY table!
                # Set status to 3 (already in) and assign the product id (pid)
                # to the product_urls record.
                logging.info(
                    "Item already stored in db in product_details table with pid: %s, update status (3)", (row['id'])
                    )
                    
                    
                if (item['test'] == 1) or (item['test'] == '1'):    
                    tx.execute(
                        "UPDATE `product_urls` SET `status` = 3, `pid` = %s "
                        "WHERE `id` = %s",
                        (row['id'], item['id'],)
                        )
                else:
                    tx.execute(
                        "UPDATE `product_urls_SCRAPY` SET `status` = 3, `pid` = %s "
                        "WHERE `id` = %s",
                        (row['id'], item['id'],)
                        )                    
                
                logging.debug(
                    "Execution DONE, product_details table with pid: %s, update status (3) in urls", (row['id'])
                    )
                
            else:
                logging.info(
                    "New item (%s), update status (1) in product_urls table",
                     item['id']
                     )
                # No duplicates found! let's insert the product data into 
                # the product_details_SCRAPY table.
                # To do! - don't mess with the product_details_SCRAPY table for now, 
                # just only update the product_urls status for test purpose.
                # Later on need to make the script store the new product to
                # the product_details_SCRAPY table.
                
                # Not yet in the product_details_SCRAPY_SCRAPPY table, store it as a new record. /* ADDED By Ronald */
                # Insert the product in the product_details_SCRAPY table       #TEST TABLE
                # Insert the table with: id, source, link, url
                # title, list, price, stars, reviews, stock, description
                if (item['test'] == 1) or (item['test'] == '1'):
                    tx.execute(
                        "INSERT INTO `product_details` (`source`, `title`, `link`, `list`, `price`, `stars`, `reviews`, `stock`, `description`, `added`, `updated`, `active`, `url_hash`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, MD5(%s))",
                        (item['source'], item['title'], item['affiliate_link'], item['list'], item['price'], item['stars'], item['reviews'], item['stock'], item['description'], time.time(), time.time(), '9', item['url'])
                        )
                else:
                    tx.execute(
                        "INSERT INTO `product_details_SCRAPY` (`source`, `title`, `link`, `list`, `price`, `stars`, `reviews`, `stock`, `description`, `added`, `updated`, `active`, `url_hash`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, MD5(%s))",
                        (item['source'], item['title'], item['affiliate_link'], item['list'], item['price'], item['stars'], item['reviews'], item['stock'], item['description'], time.time(), time.time(), '9', item['url'])
                        )                   
                
                # Select the last id for logging purpose to check wich id belongs to which PID
                tx.execute(
                    "SELECT LAST_INSERT_ID() as id"
                    )               
                productid = tx.fetchone()
                
                
                if (item['test'] == 1) or (item['test'] == '1'):
                    tx.execute(
                        "UPDATE `product_urls` SET `status` = 1, `pid` = %s, `cat` = %s, `sub` = %s, `subsub` = %s WHERE `id` = %s",
                        (productid['id'], item['cat'], item['sub'], item['subsub'], item['id'],)
                        )
                else:
                    tx.execute(
                        "UPDATE `product_urls_SCRAPY` SET `status` = 1, `pid` = %s, `cat` = %s, `sub` = %s, `subsub` = %s WHERE `id` = %s",
                        (productid['id'], item['cat'], item['sub'], item['subsub'], item['id'],)
                        )
                
                logging.info(
                    "Item %s from product_urls stored in product_details as %s, this is same as the PID in product_urls", 
                    item['id'], productid
                    )      
          
    def handle_error(self, e):
        logging.error(e)     

class MySQLUpdateProduct(object):


    def open_spider(self, spider): 
    
        # set db pool by using the custom build mysql_adbapi_connection module.
        if hasattr(spider, 'eu'): 
            self.dbpool = mysql_adbapi_connection.setup_eu_conn_adbapi()
        else:
            self.dbpool = mysql_adbapi_connection.setup_conn_adbapi()
    
        logging.basicConfig(
            filemode='w', level=logging.INFO)  
            
        log_path = spider.settings.get('LOG_FILE')

        open(
            '%s' % log_path, 
            'w')

        logging.info(
            "We are running this spider: %s",
            spider.name)
            
            
        # Check if the spider also updates the categories, descriptions or images
        # If 0 than not. If 1 update cat, subcat and subsubcat
        self.updateCats = spider.updateCategories
        self.updateDescriptions = spider.updateDescriptions
        self.updateImages = spider.updateImages
            
    def close_spider(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()        
 
    # The function which actually handles the spider item yields:
    def process_item(self, item, spider):
        # Run db query in thread pool to process the fully scraped product.
        # Use the _conditional_new_sku function of this class (below),
        # and feed it the item as passed along by the spider.
        # Set tables for test purposes
        if (item['test'] == 1) or (item['test']  == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (item['test']  == 0) or (item['test']  == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'
        
        if item['failed']:
            raise DropItem("We have an failed item %s", item['id'])
        else:    
            
            # When status = UpdateStatus the product is now longer active
            if item['pipeline'] is 'UpdateStatus':
                query = self.dbpool.runInteraction(self._conditional_update_status, item)
                query.addErrback(self.handle_error) 
                
                try:
                    self.dbpool.runInteraction(self._conditional_update_status, item)
                    
                except MySQLdb.OperationalError, e:
                    if e[0] not in (2006, 2013):
                        raise
                    log.msg("%s got error %s, retrying operation" % (self.__class__.__name__, e))
                    
                    conn = self.connections.get(self.threadID())
                    self.disconnect(conn)
                    
                    # set db pool by using the custom build mysql_adbapi_connection module.
                    if hasattr(spider, 'eu'): 
                        self.dbpool = mysql_adbapi_connection.setup_eu_conn_adbapi()
                    else:
                        self.dbpool = mysql_adbapi_connection.setup_conn_adbapi()
                        self.dbpool.runInteraction(self._conditional_update_status, item)
            
            # When status = UpdateProduct the product is still active and need to be updated          
            elif item['pipeline'] is 'UpdateProduct': 
                # query = self.dbpool.runInteraction(self._conditional_update_product, item)
                # query.addErrback(self.handle_error)

                try:
                    self.dbpool.runInteraction(self._conditional_update_product, item)
                    
                except MySQLdb.OperationalError, e:
                    if e[0] not in (2006, 2013):
                        raise
                    log.msg("%s got error %s, retrying operation" % (self.__class__.__name__, e))
                    
                    conn = self.connections.get(self.threadID())
                    self.disconnect(conn)
                    
                    # set db pool by using the custom build mysql_adbapi_connection module.
                    if hasattr(spider, 'eu'): 
                        self.dbpool = mysql_adbapi_connection.setup_eu_conn_adbapi()
                    else:
                        self.dbpool = mysql_adbapi_connection.setup_conn_adbapi()
                        self.dbpool.runInteraction(self._conditional_update_product, item)

            return item
 
    def _conditional_update_product(self, tx, item):
        
        # We are going to update the product in the urls as details table
        logging.info(
            "Updating item from {0} with id: {1}".format(self.urls_table, item['id'])
            )
            
        # First check if there is a NULL, happens for old products. 
        query = ("SELECT `id` "
                "FROM `{0}` "
                "WHERE `id` = %s AND `url_hash` IS NULL ".format(self.details_table)
        )    
        
        tx.execute(query,
            (item['pid'],)
            )
            
        isnull = tx.fetchone() 
        
        if isnull:
            logging.info(
                "Product with details id has a NULL url_hash value: {0}".format(item['pid'])
                )
        
            query = ("UPDATE `{0}` As details "
                    "INNER JOIN `{1}` As urls "
                    "ON details.id = urls.pid "
                    "SET details.list=%s, details.price=%s, details.stars=%s, details.reviews=%s, details.stock=%s, details.updated=%s, details.url_hash=%s, urls.processing = 0 "
                    "WHERE details.id = %s".format(self.details_table, self.urls_table)
                )
            
            tx.execute(query, 
                (item['list'], item['price'], item['stars'], item['reviews'], item['stock'], time.time(), item['url_hash'], item['pid'] )
                )
                
            logging.info(
                "Updated product and set url_hash for details id: {0}".format(item['pid'])
                )
        else:
            """
            #  Check if there is a match between the product in the urls and details table
            query = ("SELECT `id` "
                "FROM `{0}` "
                "WHERE `url_hash` = %s ".format(self.details_table)
                )
            
            tx.execute(query,
                (item['url_hash'],)
                )
        
            updated = tx.fetchone() 
        
            # If match is correct, then update the fields: list, price, stars, reviews, stock and of course update time
            if updated:
            """
            
            
            # Update DESCRIPTIONS Code! Added 22-05-2017
            if ( self.updateDescriptions == 1 or self.updateDescriptions == '1' ):
                query = ("UPDATE `{0}` As details "
                        "INNER JOIN `{1}` As urls "
                        "ON details.id = urls.pid "
                        "SET details.list=%s, details.price=%s, details.stars=%s, details.reviews=%s, details.stock=%s, details.updated=%s, details.description=%s, urls.processing = 0 "
                        "WHERE details.url_hash = %s AND details.id = %s".format(self.details_table, self.urls_table)
                )
                
                tx.execute(query, 
                    (item['list'], item['price'], item['stars'], item['reviews'], item['stock'], time.time(), item['description'], item['url_hash'], item['pid'])
                    ) 
                    
            else:
                query = ("UPDATE `{0}` As details "
                        "INNER JOIN `{1}` As urls "
                        "ON details.id = urls.pid "
                        "SET details.list=%s, details.price=%s, details.stars=%s, details.reviews=%s, details.stock=%s, details.updated=%s, urls.processing = 0 "
                        "WHERE details.url_hash = %s AND details.id = %s".format(self.details_table, self.urls_table)
                )
                
                tx.execute(query, 
                    (item['list'], item['price'], item['stars'], item['reviews'], item['stock'], time.time(), item['url_hash'], item['pid'])
                    ) 

            # Update Categories Code! Added 06-10-2016
            if (self.updateCats == 1 or self.updateCats == '1'):
            
                query = ("UPDATE `{0}` "
                        "SET `cat` = %s, `sub` = %s, `subsub` = %s "
                        "WHERE `url_hash` = %s AND `id` = %s".format(self.urls_table)
                )
                
                tx.execute(query, 
                    (item['cat'], item['sub'], item['subsub'], item['url_hash'], item['id'])
                    )  

                logging.info(
                    "Categories Item updated in {0}: {1}".format(self.urls_table, item['pid'])
                    )   
                    
            # Old Image Link Update Code! Added 13-12-2016
            if (self.updateImages == 1 or self.updateImages == '1'): 
                
                # Setting Image_status 9 for OLD thumbs purpose
                # Delete later!!
                query = ("UPDATE `{0}` "
                        "SET `img` = %s, `img2` = %s, `img3` = %s, `img_status` = 9 "
                        "WHERE `url_hash` = %s AND `id` = %s".format(self.urls_table)
                )
                
                tx.execute(query, 
                    (item['img1'], item['img2'], item['img3'], item['url_hash'], item['id'])
                    )  

                logging.info(
                    "Images Item updated in {0}: {1}".format(self.urls_table, item['pid'])
                    )  
                    

    def _conditional_update_status(self, tx, item):    
        # When the product url does not exits anymore we have to change status fields
        logging.info(
            "Because of 404 response, update status to 4 in {0} with id: {1}".format(self.urls_table, item['id']))

        # First check if there is a NULL, happens for old products. 
        query = ("SELECT `id` "
        "FROM `{0}` "
        "WHERE `id` = %s AND `url_hash` IS NULL ".format(self.details_table)
        )    
        
        tx.execute(query,
            (item['pid'],)
            )
            
        isnull = tx.fetchone() 
        
        if isnull:
            logging.info(
                "Product with details id has a NULL url_hash value: {0}".format(item['pid'])
                )
        
            # Set the product in status 4 in the urls table
            query = ("UPDATE `{0}` "
                "SET `status`= 4, `processing` = 0 "
                "WHERE `id` = %s".format(self.urls_table)
                )

            tx.execute(query,
                (item['id'],)
                )   

            # Set the product to active 0 in the details table
            query = ("UPDATE `{0}` "
                "SET `active`= 0, `updated` = %s, `url_hash` = %s "
                "WHERE `id` = %s".format(self.details_table)
                )
            
            tx.execute(query,
                (time.time(), item['url_hash'], item['pid'],)
                )                
        
        else:
            # Check if there is a match between the product in the urls and details table
            query = ("SELECT `id` "
                "FROM `{0}` "
                "WHERE `url_hash` = %s".format(self.details_table)
                )
            
            tx.execute(query,
                (item['url_hash'],)
                )
            
            updated = tx.fetchone()             
            
            if updated:
                # Set the product in status 4 in the urls table
                query = ("UPDATE `{0}` "
                    "SET `status`= 4, `processing` = 0 "
                    "WHERE `id` = %s".format(self.urls_table)
                    )

                tx.execute(query,
                    (item['id'],)
                    )
                
                # Set the product to active 0 in the details table
                query = ("UPDATE `{0}` "
                    "SET `active`= 0, `updated` = %s "
                    "WHERE `url_hash` = %s".format(self.details_table)
                    )
                
                tx.execute(query,
                    (time.time(), item['url_hash'],)
                    )

                logging.info(
                    "Item set to active = 0 in {0}: {1}".format(self.details_table, updated['id'])
                    ) 
            
            # If there is no match, something is really wrong. Drop the item from the database and give a Critical Error
            else: 
                logging.critical("There is a URL_HASH mismatch, Do Nothing")

            
    def handle_error(self, e):
        logging.error(e) 
 