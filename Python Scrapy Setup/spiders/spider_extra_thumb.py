import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
import urlparse
import product_scrape_xpaths
from scraper1.items import ScraperImageItem

import MySQLdb
import mysql_connection
import logging
from datetime import datetime
import time
from slugify import slugify
import pprint 
from scrapyd_api import ScrapydAPI
import re

class ThumbExtraSpider(scrapy.Spider):
    # Set the Pipeline to be used after scraping
    handle_httpstatus_list = [404]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper1.pipelines.pipelines_thumbs.ThumbsExtraPipeline': 100                    
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scraper1.middlewares.redirect.RedirectMiddleware': None
        }
    }
    
    # Set the short-name for this spider:
    name = "ScrapeExtraThumbs"
    # Restrict the domain name which the spider can operate on.
    # Make sure to append the list for new sources.
    allowed_domains = [
        "amazonaws.com", #For Sources which have their pictures on the Amazon Cloud
        "dx.com",
        "dxcdn.com",
        "banggood.com",
        "focalprice.com",
        "miniinthebox.com", #Tmart Images
        "tmart.com",
        "image-tmart.com"
        "gearbest.com",
        "tinydeal.com",
        "geekbuying.com",
        "lightinthebox.com",
        "dealsmachine.com",
        "newfrog.com",
        "tomtop.com",
        "tomtop-cdn.com", #TomTop Images
        "fasttech.com",
        "chinavasion.com",
        "chv.me", #Chinavasion Img CDN
        "tvc-mall.com",
        "antelife.com",
        "cafago.com",
        "chinabuye.com",
        "dinodirect.com", 
        "sunsky-online.com",
        "cndirect.com",
        "zapals.com",
        "shein.com",
        "ltwebstatic.com", # SheIn Images 2
        "camfere.com",
        "rcmoment.com",
        "romwe.com",
        "newchic.com",
        "rotita.com"
        ]
    
    def __init__(self, test = 0, limit =0, *args, **kwargs):
        super(ThumbExtraSpider, self).__init__(*args, **kwargs)
        #self.source = source
        self.test = test
        self.limit = limit
       
        if (self.test == 1) or (self.test == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (self.test == 0) or (self.test == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'        
        
        
       # Store the source and date in a report summary variable
        self.report_summary = []
        #self.report_summary.append("Source: %s" % source)
        self.report_summary.append("Test: %s" % test)
        self.report_summary.append("Date: %s" % (
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        # Return an error in case no source code was passed along.
        """
        if self.source == 0:
            logging.critical("No source code was passed along!")
            sys.exit()
        """
        

                
    
    def start_requests(self):
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
    
    
        # Now fetch some URLs from the product_urls table.
        # Define which table to use according to Test or Real
        
        query = ("SELECT urls.source, urls.img, urls.sku, urls.pid, details.title, urls.id, urls.img2, urls.img3 "
                "FROM `{0}` As urls "
                "INNER JOIN `{1}` As details "
                "ON urls.pid = details.id "
                "WHERE urls.status = 1 AND (details.thumbs_extra = 0 OR details.thumbs_extra = 1) AND details.active = 1 AND urls.source != 19 " #SET DEALSMACHINE OFF 19
                "AND ((urls.img2 != '' OR urls.img2 IS NOT NULL) "
                "AND (urls.img3 != '' OR urls.img3 IS NOT NULL)) "
                "AND details.thumb_path_2 IS NULL AND details.thumb_path_3 IS NULL "
                "LIMIT {2} ".format(self.urls_table, self.details_table, self.limit)
            )
            
            
        # self.cursor.execute(query,(self.source,))
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        # Close the db connection when done.
        self.conn.close() 
        
        # Loop through each of the rows, as row.
        # And initiate a scrape for each of them based on the URL, 
        # also pass along the id of the row from the product_urls table as
        # meta data (for later reference), and handle it through the parse 
        # function.
        
        for row in rows:
            # images = [ row[1], row[6], row[7] ]
            # logging.info('images: %s', images) 
            if re.match('^http:\/\/[^\.]+[\.][^\.]+[\.]com[\.]*', row[1]) is not None:
                yield scrapy.Request(
                    url=row[1],
                    meta={'source': row[0], 'img': row[1], 'img2': row[6], 'img3': row[7], 'pid': row[3], 'title': row[4], 'sku': row[2], 'id': row[5]}, 
                    callback=self.parse,
                    errback=self.errback)  
            else:
                logging.error('Request Error: %s', row[1])
                continue

    def errback(self, failure):
        # log all failures
        logging.error(repr(failure))

                    
    def parse(self, response):
        
        source = response.meta['source']
        item = ScraperImageItem()
        
        if response.status == 404:
            # Complete the item for the use in the pipeline
            image_name = response.meta['title'] + '-' + response.meta['sku']
            
            # Set default image urls list
            item['image_urls'] = []
            
            
            item['id'] = response.meta['id']
            item['pid'] = response.meta['pid']
            item['image_name'] = slugify(image_name, to_lower=True)
            item['test'] = self.test
            item['source'] = source
            item['pipeline'] = 'ErrorImage'
  
            yield item
            
        else:
            # Complete the item for the use in the pipeline
            image_name = response.meta['title'] + '-' + response.meta['sku']
            
            # Set default image urls list
            item['image_urls'] = []
            
            # Check if img exist
            if response.meta['img2']:
                item['image_urls'].append( response.meta['img2'] )
            if response.meta['img3']:
                item['image_urls'].append( response.meta['img3'] )
            
            
            item['id'] = response.meta['id']
            item['pid'] = response.meta['pid']
            item['image_name'] = slugify(image_name, to_lower=True)
            item['test'] = self.test
            item['source'] = response.meta['source']
            item['pipeline'] = 'SaveImage'
            
            yield item
    
    def count_new_thumbs(self):
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
                
        query = ("SELECT COUNT(*) "
                "FROM `{0}` As urls "
                "INNER JOIN `{1}` As details "
                "ON urls.pid = details.id "
                "WHERE urls.status = 1 AND (details.thumbs_extra = 0 OR details.thumbs_extra = 1) AND details.active = 1 AND urls.source != 19 " #SET DEALSMACHINE OFF 19
                "AND ((urls.img2 != '' OR urls.img2 IS NOT NULL) "
                "AND (urls.img3 != '' OR urls.img3 IS NOT NULL)) "
                "AND details.thumb_path_2 IS NULL AND details.thumb_path_3 IS NULL ".format(self.urls_table, self.details_table)
            )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        
        # Close the db connection when done.
        self.conn.close() 
        
        self.items_left = result[0]
        
        logging.info('(Re)Run, there are %s products left', str(self.items_left))       
        
    def closed(self, reason):
        # join all the report summary strings together, 
        # with a new line '\n' in between
        stats = self.crawler.stats.get_stats()
        stats = pprint.pformat(stats)
        s = '\n'.join(self.report_summary)
        # log the summary report as stored in 's'
        logging.info(s)
    
        # Store the log to our mysql db if it's not a test run
        # Open the log file and retrieve its content
        log_path = self.settings.get('LOG_FILE')
        file = open(
            '%s' % log_path, 
            'r')
        file_content = file.read()
        file.close()
        
        
        # Store the log to our mysql db
        
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
                
        self.cursor.execute(
            "INSERT INTO `scrapy_logs` "
            "(`spider`, `test`,`log_date`, `log_file`, `stats`, `short_msg`, `long_msg`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('spider_thumbs', self.test, time.time(), log_path, stats, s, file_content)
            )
        self.conn.commit()
        
        # Close the db connection when done.
        self.conn.close() 
        
        # Count the products still need to be done
        self.count_new_thumbs()
        

        # Check if we need to rerun the script.
        # Force the spider to stop when we cancel the job
        
        if reason is 'finished':   
            if self.items_left >= 200 and int(self.limit) >= 51:
                if (self.test == 1) or (self.test == '1'):
                    scrapyd = ScrapydAPI('http://127.0.0.1:6800')
                    scrapyd.schedule('scraper1', 'ScrapeExtraThumbs', test='1', limit=self.limit)
                else:
                    logging.info ("Don't Reschedule because it's a test run") 
       