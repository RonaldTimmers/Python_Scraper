# Python Module to help validate Xpath extracts.
# Author(s): Ward Huisman

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.exceptions import DropItem
import logging
import re
import sys



# Used @ x_description function
# Bleach is a allowed-list-based HTML sanitizing library that escapes or strips markup and attributes.
# https://bleach.readthedocs.io/en/latest/

import bleach
import mistune

# BeautifulSoup4 for editing/removing the incoming html
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

# Define function to check if any text was returned
def x_string(wrapper, xp, empty_error, wildcard = 0):
	# Try to extract from the wrapper, based on the xpath (xp).
    xp_extract = wrapper.xpath(xp).extract()
    #logging.debug("We extracted this: %s", xp_extract)
    
    if xp_extract:
        # There is something extracted,
       
        # Extra Check if it is not an empty string 
        if xp_extract[0] == "" and wildcard == 0:
            return 'Empty'
        
        # use the first instance for the return string.
        return_str = xp_extract[0]
        
        # Further clean-up is needed, saved for later improvements.
        return_str = return_str.strip(' \t\n\r')
        return_str = return_str.replace(u'\xa0', ' ')
        return_str = return_str.replace(u'\u25bc', '')
    else:
        # Nothing there, set the return string to an empty space 
        return_str = ""
        # And throw out an error if needed, and exit the program
        if empty_error == 1 and wildcard == 0:
            logging.critical("Xpath (%s) extract returned empty!", xp)
            #sys.exit()
            return 'Empty'
            #raise CloseSpider('empty return string')
    # Return the return string as stored in return_str
    return return_str


# Define function to check if anything was returned and strip away any 
# letters from the string (e.g. USD) to keep only numbers and dots 
# (to facilitate decimal numbers).
def x_decimal(wrapper, xp, empty_error, wildcard = 0):
    # Try to extract from the wrapper, based on the xpath (xp).
    xp_extract = wrapper.xpath(xp).extract()
    #logging.debug("We extracted this: %s", xp_extract)
    if xp_extract:
        # there is a valid xpath extraction, 
        # use the first instance for the returned float
        # make sure to remove any text characters to only keep 
        # the float / decimal number using regex (re)
        non_decimal = re.compile(r'[^\d.]+')
        return_fl = non_decimal.sub('', xp_extract[0])
        #logging.debug("What we return: %s", return_fl)
    else:
        # nothing there, return default: zero
        return_fl = 0
        # and throw out an error if needed
        if empty_error == 1 and wildcard == 0:
            logging.critical("Xpath (%s) extract returned empty!", xp)
            #sys.exit()
            return 'Empty'
            #raise CloseSpider('empty return decimal')
    return return_fl


# Define function to handle the 'in-stock' check.
def x_stock(wrapper, xp, empty_error, source, wildcard = 0):
    # Try to extract from the wrapper, based on the xpath (xp).
    xp_extract = wrapper.xpath(xp).extract()
    if xp_extract:
        # There is something extracted, 
        # use the first instance for the return string.
        stock_str = ''.join(xp_extract)
        # Check the string for certain condition to determine whether it is
        # in or out of stock. Will be slightly different per source so might
        # need to build further if/else/or statements into it.
        logging.debug("The Stock string: %s", stock_str)
        # Source: DX - 2
        if source == "2":
            if "PauseSale" in stock_str:
                return_int = 1
            else:
                return_int = 0
        # Source: Banggood - 4 
        elif source == "4" or source == "4_EU":
            if "Sold Out" in stock_str:
                return_int = 1
            else: 
                return_int = 0       
        # Source: Focalprice - 5
        elif source == "5":
            if "Sold Out" in stock_str:
                return_int = 1
            else: 
                return_int = 0
        # Source: Dealsmachine - 19 
        elif source == "19":
            if "Out of stock" in stock_str:
                return_int = 1
            else: 
                return_int = 0
        # Source: Gearbest - 28 
        elif source == "28":
            if "Add to Cart" in stock_str:
                return_int = 0
            else: 
                return_int = 1
        # Source: Miniinthebox - 6  AND lightinthebox - 25             
        elif source == "6" or source == "25":
            if "Out Of Stock" in stock_str:
                return_int = 1
            else: 
                return_int = 0     
                
        # Source: Tmart - 7                
        elif source == "7":
            if "Add to Cart" in stock_str:
                return_int = 0
            else: 
                return_int = 1
        
        # Source: TInyDeal - 20                
        elif source == "20":
            if  "discontinued" in stock_str:
                return_int = 1
            else: 
                return_int = 0    
                
        # Source: Geekbuying - 31          
        elif source == "31":
            if  "Add" not in stock_str:
                return_int = 1
            else: 
                return_int = 0 

        # Source: Newfrog - 29          
        elif source == "29":
            if  "in stock" not in stock_str:
                return_int = 1
            else: 
                return_int = 0     
        # Source: Tomtop - 15  and TVC-Mall - 30  and AnteLife - 63
        elif source == "15" or source == "30" or source == "63":
            if  "In Stock" not in stock_str:
                return_int = 1
            else: 
                return_int = 0  
        # Source:  Chinavasion - 9  and ChinaBuye - 10  and Zapals - 66   
        elif source == "9" or source == "10" or source == "66":
            if  "In stock" not in stock_str:
                return_int = 1
            else: 
                return_int = 0                   
        # Source: Fasttech - 22          
        elif source == "22":
            if  "in_stock" not in stock_str:
                return_int = 1
            else: 
                return_int = 0   
        # Source: Cafago - 64          
        elif source == "64":
            if  "1" in stock_str:
                return_int = 0
            else: 
                return_int = 1  
        # Source: Dinodirect - 8      
        elif source == "8":
            if  "newaddtocart" in stock_str:
                return_int = 0
            else: 
                return_int = 1     
        # Source: SunSky Online - 21      
        elif source == "21":
            if  "Lead Time" in stock_str:
                return_int = 0
            else: 
                return_int = 1   
        # Source: CNDirect - 65      
        elif source == "65":
            if "Out Of Stock" in stock_str:
                return_int = 1
            else: 
                return_int = 0      
        # Source: SheIn - 59      
        elif source == "59":
            if "Add To Bag" in stock_str:
                return_int = 0
            else: 
                return_int = 1    
        # Source: Camfere - 67 or RCmoment - 68  
        elif source == "67" or source == "68":
            if "1" in stock_str:
                return_int = 0
            else: 
                return_int = 1            
        # Source: Romwe - 55   
        elif source == "55":
            if stock_str == "0":
                return_int = 1
            else: 
                return_int = 0  
        # Source: NewChic - 69   
        elif source == "69":
            if "in stock" in stock_str:
                return_int = 0
            else: 
                return_int = 1  
                
        # Source: Rotita - 71   
        elif source == "71":
            if "InStock" in stock_str:
                return_int = 0
            else: 
                return_int = 1 
                
    else:
        # Nothing there, set stock to 1 by default
        return_int = 0
        # And throw out an error if needed, and exit the program
        if empty_error == 1 and wildcard == 0:
            logging.critical("Xpath (%s) extract returned empty!", xp)
            #sys.exit()
            return 'Empty'
            #raise CloseSpider('empty return stock')
    # Return the stock integer as stored in return_int
    logging.debug("What do we return: %d", return_int)
    return return_int


# Define function to check and process a description text.
def x_description(wrapper, xp, empty_error, wildcard = 0):
    # Try to extract from the wrapper, based on the xpath (xp).
    xp_extract = wrapper.xpath(xp).extract()
    if xp_extract:
        # There is something extracted,
        # join all text values returned from the nodes listed within the xpath.
        descr_str = " ".join(xp_extract)
     
        
        
        # Remove starting or trailing white spaces, new lines and tabs.
        descr_str = descr_str.strip(' \t\n\r')
        # Further clean-up is needed, saved for later improvements.
        descr_str = descr_str.replace(u'\n', '')        # New line
        descr_str = descr_str.replace(u'\r', '')        # Carriage Return
        descr_str = descr_str.replace(u'\t', '')        # Tab
        
        logging.debug("What for descr_str o we return: %s", descr_str)
        
        descr_str = descr_str.replace(u'\xa0', ' ')     # Non Breaking Space
        descr_str = descr_str.replace(u'\u25cf', ' ')   # Black Circle
        descr_str = descr_str.replace(u'h1', 'h4')      # Header to H4
        descr_str = descr_str.replace(u'h2', 'h4')      #
        descr_str = descr_str.replace(u'h3', 'h4')      # 
        descr_str = descr_str.replace(u'h5', 'h4')      # 
        descr_str = descr_str.replace(u'h6', 'h4')      # Header to H4
        descr_str = descr_str.replace(u'<i>,</i>', ' ')             # Remove , comma after word in Table Cell - Extra for LITB and MITB
        descr_str = descr_str.replace(u'[email protected]', ' ')    # Email addresses converted to protected, remove!
        
        
        
        soup = BeautifulSoup(descr_str, "lxml") # Get the string and create a soup! With the lxml parser(default)

        # Loop through the created soup object and delete te inidicated tags
        for tags in soup.find_all(['i', 'style', 'script', 'iframe']):
            tags.decompose()

        # When done with deleting the needed tags, get back to a unicode string to 
        # Santizie with Bleach
        descr_str = unicode (soup)
        
        
        # logging.debug("What for i_tag do we return: %s", soup)

        # descr_str = descr_str.encode(encoding='UTF-8',errors='ignore')
        # descr_str = mistune.markdown(descr_str, escape=False, hard_wrap=True)
        
       
        
        # Use the Bleach Module to extract still unwanted tags in the HTML 
        # (In this case when <script> still exists will be shut down)
        # JS can't get triggered in that manner
        
        # We only allow the following tags
        # Not allowed e.a : script, link, a 
        descr_str = bleach.clean(descr_str, tags=[u'em', u'li', u'ol', u'ul', u'p', u'table', u'tbody', u'tr', u'td', u'th', u'h4', u'br', u'b', u'strong', u'span', u'div' ], strip=True)
        
        
        
        
        
        # If there are more than three <br> variants in a row. Replace it with just one tag
        descr_str = re.sub(u'(\s*<br[^>]*>){3,}', '<br>', descr_str);
        
        # Strip down all the whitespace between html <tags>
        regex = re.compile(r"\s*(<(?![\/]?strong)[^<>]+>)\s*") # re.compile(r"\s*(<[^<>]+>)\s*")
        descr_str = regex.sub("\g<1>", descr_str)
        
    else:
        # Nothing there, set the return string to an empty space 
        descr_str = ""
        # And throw out an error if needed, and exit the program
        if empty_error == 1 and wildcard == 0:
            logging.critical("Xpath (%s) extract returned empty!", xp)
            #sys.exit()
            return 'Empty'
            
            #raise CloseSpider('empty return description')
    # Return the description string as stored in descr_str
    # logging.debug("What for description do we return: %s", descr_str)
    return descr_str
    
