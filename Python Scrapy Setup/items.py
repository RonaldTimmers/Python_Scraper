# -*- coding: utf-8 -*-

# Define here the models for your scraped items

#
# See documentation in:

# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

# The item to store new product URL link information in
class ScraperURLItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    pipeline = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    failed = scrapy.Field()
    test = scrapy.Field()
    url_query = scrapy.Field()


# The item to store complete product information in
class ScraperProductItem(scrapy.Item):
    id = scrapy.Field()
    source = scrapy.Field()
    pipeline = scrapy.Field()
    url = scrapy.Field()
    affiliate_link = scrapy.Field()
    title = scrapy.Field()
    img1 = scrapy.Field() 
    img2 = scrapy.Field() 
    img3 = scrapy.Field() 
    # image_urls = scrapy.Field()           # CHANGED!!!! image_url to image_urls, list op scraped image urls
    # images = scrapy.Field()             # CHANGED!!!! added new field images
    # image_paths = scrapy.Field()    # CHANGED!!!! added new field images, location of image on localhost
    list = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    reviews = scrapy.Field()
    stock = scrapy.Field()
    sku = scrapy.Field()
    description = scrapy.Field()
    cat = scrapy.Field()
    sub = scrapy.Field()
    subsub = scrapy.Field()
    failed = scrapy.Field()
    test = scrapy.Field()


# The item to store complete product information in
class ScraperUpdateItem(scrapy.Item):
    id = scrapy.Field()
    pid = scrapy.Field()
    source = scrapy.Field()    
    pipeline = scrapy.Field()
    #link = scrapy.Field()    
    url_hash = scrapy.Field()    
    list = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    reviews = scrapy.Field()
    stock = scrapy.Field()
    description = scrapy.Field()
    img1 = scrapy.Field() 
    img2 = scrapy.Field() 
    img3 = scrapy.Field() 
    cat = scrapy.Field()
    sub = scrapy.Field()
    subsub = scrapy.Field()
    #sku = scrapy.Field()
    failed = scrapy.Field()
    test = scrapy.Field()
    
    
# The item to store complete product information in
class ScraperUpdateOldItem(scrapy.Item):
    id = scrapy.Field()
    source = scrapy.Field()    
    pipeline = scrapy.Field()
    link = scrapy.Field()    
    url_hash = scrapy.Field()    
    list = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    reviews = scrapy.Field()
    stock = scrapy.Field()
    sku = scrapy.Field()
    failed = scrapy.Field()
    test = scrapy.Field()
    thumb = scrapy.Field()
    cat = scrapy.Field()
    sub = scrapy.Field()
    subsub = scrapy.Field()

class ScraperImageItem(scrapy.Item):    
    image_urls = scrapy.Field()           # CHANGED!!!! image_url to image_urls, list op scraped image urls
    images = scrapy.Field()             # CHANGED!!!! added new field images
    image_paths = scrapy.Field()    # CHANGED!!!! added new field images, location of image on localhost
    id = scrapy.Field()
    pid = scrapy.Field()
    image_name = scrapy.Field()
    source = scrapy.Field()
    test = scrapy.Field()
    pipeline = scrapy.Field()

class ScraperOldImageItem(scrapy.Item):    
    image_urls = scrapy.Field()           # CHANGED!!!! image_url to image_urls, list op scraped image urls
    images = scrapy.Field()             # CHANGED!!!! added new field images
    image_paths = scrapy.Field()    # CHANGED!!!! added new field images, location of image on localhost
    id = scrapy.Field()
    thumb_path = scrapy.Field()
    source = scrapy.Field()
    test = scrapy.Field()
    pipeline = scrapy.Field()








































































































    description = scrapy.Field()





