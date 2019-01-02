import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from scrapy.http import Request
from scraper1.items import ScraperImageItem, ScraperOldImageItem
from scrapy.utils.project import get_project_settings

from twisted.enterprise import adbapi

import MySQLdb
import mysql_connection
import mysql_adbapi_connection

import logging
import time                                         
import os, sys
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
    
from scrapy.utils.misc import md5sum

from PIL import Image, ImageOps, ImageEnhance
from datetime import datetime
import six

class ThumbsPipeline(ImagesPipeline):
    
    def media_to_download(self, request, info):
        self.settings = get_project_settings()
    
    
    def get_media_requests(self, item, info):
        for index, image_url in enumerate(item['image_urls']):
            yield scrapy.Request(image_url, meta={'source': item['source'], 'image_name': item['image_name'], 'image_number': index})
    
    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            
            # They save the image Here!
            try:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
                logging.info('We store the following path: %s', path);
            except:
                logging.critical('We did not store the following path: %s', path);
                sys.exit()
            else:
                logging.info('Image_downloaded Checksum: %s', checksum);
                return checksum

    def get_images(self, response, request, info):
        # path = self.file_path(request, response=response, info=info) //Removed, don't need to set path of Full/ Images
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        # image, buf = self.convert_image(orig_image)
        # yield path, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(orig_image, size)
            yield thumb_path, thumb_image, thumb_buf
    
   
   # Inherithed from pipelines.images, did some quality tweaks.
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG', subsampling=0, quality=95)   
        
        return image, buf
    
    # Copied from pipelines.images, did some simple quality tweaks.

    def file_path(self, request, response=None, info=None):
        # Custom added by Ronald
        # Used for custom save path
        save_date = datetime.utcnow()
        image_name = request.meta['image_name'] # Like this you can use all from item, not just url.
        image_number = request.meta['image_number']
        last_char = image_name[-1:]
        source = request.meta['source'] # Like this you can use all from item, not just url.
        
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        #image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        #return 'full/%s.jpg' % (image_guid) #DELETED RONALD

        if (image_number in (1, 2)):
            image_number = '_' + str(image_number)
        else:
            image_number = ''
        
        full_path = str(source) + '/' + str(save_date.year) + '/' + str(save_date.month) + '/' + str(last_char) + '/' + str(image_name) + str(image_number)
        return 'thumbs/%s.jpg' % (full_path) 
    
  
    # Copied from pipelines.images, did some simple quality tweaks.   
    def thumb_path(self, request, thumb_id, response=None, info=None):
        # Custom added by Ronald
        # Used for custom save path
        save_date = datetime.utcnow()       
        image_number = request.meta['image_number']
        source = request.meta['source'] # Like this you can use all from item, not just url.
        
        
        image_name = request.meta['image_name'] # Like this you can use all from item, not just url.
        last_char = image_name[-1:]
        
        
        # start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from thumb_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if thumb_key() method has been overridden
        if not hasattr(self.thumb_key, '_base'):
            _warn()
            return self.thumb_key(url, thumb_id)
        # end of deprecation warning block

        if (image_number in (1,2)):
            image_number = '_' + str(image_number)
        else:
            image_number = ''
        
        
        # thumb_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        thumb_path = 'thumbs/' + str(source) + '/' + str(save_date.year) + '/' + str(save_date.month) + '/' + str(last_char) + '/' + str(image_name) + str(image_number)
        return '%s.jpg' % (thumb_path) 

    
    
    
    def item_completed(self, results, item, info):
        if (item['test'] == 1) or (item['test']  == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (item['test']  == 0) or (item['test']  == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
                
        if item['pipeline'] == 'ErrorImage':
            logging.info("Update imgStatus to 3 (because failed result) in %s", self.urls_table)

            # Set image_status to 3 if first thumb not exist
            query = ("UPDATE `{0}` " 
            "SET `img_status` = 3 "
            "WHERE `id` = %s".format(self.urls_table)
            )
            self.cursor.execute(query,(item['id'],))
            self.conn.commit()
            self.conn.close() 
        
            raise DropItem("Item contains no first image")
            
            
        # image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        """
        # image_paths = [x['path'] for ok, x in results if ok]
        """
        checksum = [x['checksum'] for ok, x in results if ok]
        if checksum:

            # Counter for the number of results
            i = 0;
            # Create the dictionary to dynamic build up the needed query
            parameter_dict = {'pid': item['pid']};
            for result in [x for ok, x in results if ok]:
                
                # logging.info("Item_completed result['path']: %s", result['path']);
                
                i += 1;
                # item['image_paths'].append( result['path'] )   
                
                if (i == 1):
                    parameter_dict['thumb'] = result['path']
                    set_query = " `thumb_path` =  %(thumb)s, "
                
                
                if (i == 2):
                    parameter_dict['thumb_2'] = result['path']
                    
                    set_query += " `thumb_path_2` =  %(thumb_2)s, "
                
                
                if (i == 3):
                    parameter_dict['thumb_3'] = result['path']
                    set_query += " `thumb_path_3` =  %(thumb_3)s, "
                
            parameter_dict['saved'] = i
                
            logging.info("parameter_dict: %s", parameter_dict)        
            
            
            # If image saved succesfully change img_status in product_urls table
            # And update thumb_path in product_details
            query = ("UPDATE `{0}` "
            "SET {1} `thumbs_extra` = %(saved)s " 
            "WHERE `id` = %(pid)s ".format(self.details_table, set_query)
            )
            
            # logging.info("Query: %s", query)
            
            self.cursor.execute(query,(parameter_dict))
            
            # Set image_status to 2 if one main thumb exist
            query = ("UPDATE `{0}` " 
            "SET `img_status` = 2 "
            "WHERE `id` = %s".format(self.urls_table)
            )
            self.cursor.execute(query,(item['id'],))
            self.conn.commit()
            self.conn.close()    

            return item
        
        else:
            raise DropItem("Item contains NO IMAGES")
        
        
class ThumbsOldPipeline(ThumbsPipeline):

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        #image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        #return 'full/%s.jpg' % (image_guid) #DELETED RONALD
        # Custom added by Ronald
        # Use already existing path thumb_path
        thumb_path = request.meta['thumb_path'] # Like this you can use all from item, not just url.
        full_path = thumb_path.replace('thumbs/', 'full/')
        return '%s' % (full_path) 
    
  
    # Copied from pipelines.images, did some simple quality tweaks.   
    def thumb_path(self, request, thumb_id, response=None, info=None):
        # start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from thumb_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if thumb_key() method has been overridden
        if not hasattr(self.thumb_key, '_base'):
            _warn()
            return self.thumb_key(url, thumb_id)
        # end of deprecation warning block

        # thumb_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        # Custom added by Ronald
        # Use already existing path thumb_path
        thumb_path =request.meta['thumb_path'] # Like this you can use all from item, not just url.
        return '%s' % (thumb_path) 

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'thumb_path': item['thumb_path']})
            
    
    def item_completed(self, results, item, info):
        # Setting the test values for the pipeline 
        logging.info("We are testing if 0 and real if 1: %s", item['test'])
        
        if (item['test'] == 1) or (item['test']  == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (item['test']  == 0) or (item['test']  == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'
        
        
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
        
        
        # Check if the results contain an image file
        image_paths = [x['path'] for ok, x in results if ok]
        # IF there is nog image file check first if we can update the DB
        if (not image_paths) or (item['thumb_path'] is 'thumbs/unknown.jpg'):
            # if item['pipeline'] is 'UpdateStatus'  or item['thumb_path'] is 'thumbs/unknown.jpg':
            query = ("UPDATE `{0}` As urls "
                    "INNER JOIN {1} As details "
                    "ON urls.pid = details.id "
                    "SET urls.status = 0, urls.img_status = 0, details.active = 0  "
                    "WHERE urls.id = %s".format(self.urls_table, self.details_table)
                    )
            
            self.cursor.execute(query,(item['id'],))
            
            logging.warning("Something Wrong the image of the following id: %s", item['id'])
            logging.warning("Change settings: urls.status = 0 AND urls.img_status = 0 AND details.active = 0")        
            
            self.conn.commit()
            self.conn.close() 
            
            raise DropItem("Item contains no image")

            
        # If we have an image store the results.
        item['image_paths'] = image_paths
        
        # Removing the created full image for handling the image thumb. 
        # We dont need this image right now, maybe in the future with more storage
        # Use the global variable from settings
        save_path = str(self.settings.get('IMAGES_STORE'))
        
        # Getting first element of list. If we download more images with same URL we can have more value # Maybe in the Future
        full_image_path = str(item['image_paths'][0]) 
        # Set thumb image according to full image for good coupling with database update beneath
        thumb_image_path = full_image_path.replace('full/', 'thumbs/')
        remove_path = save_path + full_image_path
        # removing
        # os.remove(remove_path)
        
        logging.debug("FULL IMAGE REMOVED: %s", remove_path)
        

       
        # If everything is oke, just update the img_status to 2 in the urls table
        if item['pipeline'] is 'UpdateImage':
            logging.info("Update Status in %s", self.urls_table)
                    
            query = ("UPDATE `{0}` " 
            "SET `img_status` = 2 "
            "WHERE `id` = %s".format(self.urls_table)
            )
            
            logging.info("Updating image to img_status = 2, following id: %s", item['id'])
            
        self.cursor.execute(query,(item['id'],))
        self.conn.commit()
        self.conn.close() 
        # self.update_counter += 1   
        # If image saved succesfully change img_status in product_urls table
        # And update thumb_path in product_details
        
        return item      




class ThumbsExtraPipeline(ImagesPipeline):
    
    def media_to_download(self, request, info):
        self.settings = get_project_settings()
    
    
    def get_media_requests(self, item, info):
        for index, image_url in enumerate(item['image_urls']):
            yield scrapy.Request(image_url, meta={'source': item['source'], 'image_name': item['image_name'], 'image_number': index})
    
    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            
            # They save the image Here!
            try:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
                logging.info('We store the following path: %s', path);
            except:
                logging.critical('We did not store the following path: %s', path);
                sys.exit()
            else:
                logging.info('Image_downloaded Checksum: %s', checksum);
                return checksum

    def get_images(self, response, request, info):
        # path = self.file_path(request, response=response, info=info) //Removed, don't need to set path of Full/ Images
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        # image, buf = self.convert_image(orig_image)
        # yield path, image, buf

        for thumb_id, size in six.iteritems(self.thumbs):
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(orig_image, size)
            yield thumb_path, thumb_image, thumb_buf
    
   
   # Inherithed from pipelines.images, did some quality tweaks.
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, 'JPEG', subsampling=0, quality=95)   
        
        return image, buf
    
    # Copied from pipelines.images, did some simple quality tweaks.

    def file_path(self, request, response=None, info=None):
        # Custom added by Ronald
        # Used for custom save path
        save_date = datetime.utcnow()
        image_name = request.meta['image_name'] # Like this you can use all from item, not just url.
        image_number = request.meta['image_number'] + 1
        last_char = image_name[-1:]
        source = request.meta['source'] # Like this you can use all from item, not just url.
        
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        #image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        #return 'full/%s.jpg' % (image_guid) #DELETED RONALD

  
        image_number = '_' + str(image_number)
        
        full_path = str(source) + '/' + str(save_date.year) + '/' + str(save_date.month) + '/' + str(last_char) + '/' + str(image_name) + str(image_number)
        return 'thumbs/%s.jpg' % (full_path) 
    
  
    # Copied from pipelines.images, did some simple quality tweaks.   
    def thumb_path(self, request, thumb_id, response=None, info=None):
        # Custom added by Ronald
        # Used for custom save path
        save_date = datetime.utcnow()
        image_name = request.meta['image_name'] # Like this you can use all from item, not just url.
        image_number = request.meta['image_number'] + 1
        last_char = image_name[-1:]
        source = request.meta['source'] # Like this you can use all from item, not just url.
        
        # start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from thumb_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if thumb_key() method has been overridden
        if not hasattr(self.thumb_key, '_base'):
            _warn()
            return self.thumb_key(url, thumb_id)
        # end of deprecation warning block

 
        image_number = '_' + str(image_number)
        
        
        # thumb_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation #DELETED RONALD
        thumb_path = 'thumbs/' + str(source) + '/' + str(save_date.year) + '/' + str(save_date.month) + '/' + str(last_char) + '/' + str(image_name) + str(image_number)
        return '%s.jpg' % (thumb_path) 

    
    
    
    def item_completed(self, results, item, info):
        if (item['test'] == 1) or (item['test']  == '1'):
            self.urls_table = 'product_urls'
            self.details_table = 'product_details'
        if (item['test']  == 0) or (item['test']  == '0'):
            self.urls_table = 'product_urls_SCRAPY'
            self.details_table = 'product_details_SCRAPY'
        try:
            # Start the db connection through the custom module.
            self.conn = mysql_connection.setup_conn()
            self.cursor = self.conn.cursor()           
        
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
                
        if item['pipeline'] == 'ErrorImage':
            logging.info("Update imgStatus to 3 (because failed result) in %s", self.urls_table)

            # Set image_status to 3 if first thumb not exist
            query = ("UPDATE `{0}` " 
                    "SET `img_status` = 3 "
                    "WHERE `id` = %s".format(self.urls_table)
            )
            self.cursor.execute(query,(item['id'],))
            self.conn.commit()
            self.conn.close() 
        
            raise DropItem("Item contains no first image")
            
            
        checksum = [x['checksum'] for ok, x in results if ok]
        if checksum:
            # Counter for the number of results
            i = 0;
            # Create the dictionary to dynamic build up the needed query
            parameter_dict = {'pid': item['pid']};
            for result in [x for ok, x in results if ok]:
                
                # logging.info("Item_completed result['path']: %s", result['path']);
                
                i += 1;
                # item['image_paths'].append( result['path'] )   
                
                if (i == 1):
                    parameter_dict['thumb_2'] = result['path']
                    set_query = " `thumb_path_2` =  %(thumb_2)s, "
                
                
                if (i == 2):
                    parameter_dict['thumb_3'] = result['path']
                    set_query += " `thumb_path_3` =  %(thumb_3)s, "
                
            parameter_dict['saved'] = i + 1
                
            logging.info("parameter_dict: %s", parameter_dict)        
            
            
            # If image saved succesfully change img_status in product_urls table
            # And update thumb_path in product_details
            query = ("UPDATE `{0}` "
                    "SET {1} `thumbs_extra` = %(saved)s " 
                    "WHERE `id` = %(pid)s ".format(self.details_table, set_query)
            )
            
            # logging.info("Query: %s", query)
            
            self.cursor.execute(query,(parameter_dict))
            
            # Set image_status to 2 if one main thumb exist
            query = ("UPDATE `{0}` " 
                    "SET `img_status` = 2 "
                    "WHERE `id` = %s".format(self.urls_table)
            )
            self.cursor.execute(query,(item['id'],))
            self.conn.commit()
            self.conn.close()    

            return item
        
        else:
            logging.info("The Product Does not Contain Extra Images: %s", item['pid'])
            
            parameter_dict = {'pid': item['pid']};
            
            # There are no extra thumbs.
            # just Change extra_thumbs from 0 to 1.
            query = ("UPDATE `{0}` "
                    "SET `thumbs_extra` = 1 " 
                    "WHERE `id` = %(pid)s ".format(self.details_table)
            )
        
            self.cursor.execute(query,(parameter_dict))
            self.conn.commit()
            self.conn.close()    

            return item      