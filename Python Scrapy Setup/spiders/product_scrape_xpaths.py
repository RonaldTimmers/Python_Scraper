# Python Module to store product scrape xpaths per source
# in a separate file.
# Author(s): Ward Huisman
# Used in Files: /spider_new_urls.py 
#                /spider_new_product.py

# Define the function to return the xpath based on the source and target.
def get_dict():
    # Initiate the sources dictionary.
    xpath_dict = {}
    
    # Create the DealExtreme dictionary (source code 2).
    xpath_dict['2'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.dx.com",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://ad.admitad.com/g/4510c4dda6205609bfdc31edb8141e/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=302497&m=32431&afftrack=CIsku&urllink=
        "affiliate_link_after": "", #?Utm_rid=19554216&Utm_source=affiliate
        # (new arrivals).
        "product_list_item": "//ul[@class='productList subList']/li",
        "product_list_title": "div[@class='pi']/p[@class='title']/a/@title",
        "product_list_url": "div[@class='pi']/p[@class='title']/a/@href",
        "next_page": "//div[@class='pageturn clearfix']/a[@class='next']/@href",
        "start_urls" : [
            "http://www.dx.com/new-arrivals",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.dx.com/sitemap",
        "sitemap_link": "//ul[@id='cateList']/li/dl/dt/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='pdetail_wrapper']",
        "title": "//div[@class='pinfo_wrapper']/h1/span[@id='headline']/@title",
        "img_url": "//ul[@class='product-small-images']/li[1]/a/@href", #//ul[@class='product-small-images']/li[1]/a/@href, //ul[@class='product-small-images']/li[2]/a/@href, //ul[@class='product-small-images']/li[3]/a/@href
        "img_url2": "//ul[@class='product-small-images']/li[2]/a/@href",
        "img_url3": "//ul[@class='product-small-images']/li[3]/a/@href",
        "list": "//del[@id='list-price']/text()",
        "price": "//span[@id='price']",
        "stars": "//b[@class='starts']/span/text()",
        "reviews": "//div[@class='review_rate']/a[@class='tu']/span",
        "sku": "//span[@class='product_sku']/span[@id='sku']/text()",
        "stock": "//input[@id='productStatus']/@value", # //ul[@class='product_detail clearfix']/li[4]/span[2]/text()
        "description": "//div[@id='overview-detailinfo']/div/node() | //div[@id='specification']/div[1]/node()", # //meta[@property='og:title']/@content | //div[@id='overview-detailinfo']/div/text()
        "cat": "//div[@class='position']/a[1]/text()",
        "sub": "//div[@class='position']/a[2]/text()",
        "subsub": "//div[@class='position']/a[3]/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }
        
    # Create the Banggood dictionary (source code 4).
    xpath_dict['4'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.banggood.com",
        "query_url":                "?currency=USD",
        "query_url_eu":             "?currency=EUR",
        "na_url":                   "",
        "affiliate_link_before":    "",
        # "affiliate_link_after":   "?currency=USD?p=5!141510275320121293",
        "affiliate_link_after":     "?p=5!141510275320121293&utm_source=bbs&utm_medium=CI&utm_content=zhangruihua",
        # (new arrivals).
        "product_list_item":        "//ul[contains(@class, 'goodlist_1')]/li",
        "product_list_title":       "span[2]/a/text()",
        "product_list_url":         "span[2]/a/@href",
        "next_page":                "//div[@class='page_num']/a[position()=last()]/@href",
        "start_urls" : [
                                    "https://www.banggood.com/new-arrivals.html",
            ],
        "start_urls_eu" : [
                                    "https://eu.banggood.com/whtop-Eu-sellers-1091.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-140.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-1697.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-896.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-133.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-155.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-1031.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-274.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-892.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-1134.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-170.html?language=en&country=150&currency=EUR",
                                    "https://eu.banggood.com/whtop-Eu-sellers-1696.html?language=en&country=150&currency=EUR", 
            ],  
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":              "https://www.banggood.com/sitemap.html",
        "sitemap_link":             "//div[@class='sitemap']/dl/dd/a[1]/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":          "//div[@class='good_main']",
        "title":                    "//div[@class='good_main']/h1/text()",
        "img_url":                  "//div[@class='good_photo_min']/ul/li[1]/a/@big", 
        "img_url2":                 "//div[@class='good_photo_min']/ul/li[2]/a/@big",
        "img_url3":                 "//div[@class='good_photo_min']/ul/li[3]/a/@big",        
        "list":                     "//div[@class='item_con']/div[3]/@oriprice", #//div[@class='old']/@oriprice
        "price":                    "//div[@class='item_con']/div[2]/@oriprice", #//div[@class='now']/@oriprice
        "stars":                    "//li[@class='review']/a/span[@itemprop='ratingValue']/text()",
        "reviews":                  "//li[@class='review']/a/span[@itemprop='reviewCount']/text()",
        "sku":                      "//input[@id='sku']/@value",
        "stock":                    "normalize-space(//div[@class='status']/text())",
        "description":              "//div[contains(@class, 'detailpage')]/div/div[@class='good_tabs_box']/div[1]/node()[not(descendant::strong[text()='More Details: '] | descendant::strong[text()='More Details:'] | descendant::strong[text()='Size Chart:'] | descendant::strong[text()='Detail Pictures'] | self::div[@class='new_size_item'])]",  # OLD normalize-space(//div[@class='good_tabs_box']/div[1])
        "cat":                      "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][2]/a/span/text()",
        "sub":                      "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][3]/a/span/text()",
        "subsub":                   "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars":          1, 
        "empty_reviews":        1,
        "empty_stock":          0,
        "empty_list":           0,
        "empty_cat":            0,
        "empty_sub":            0,
        "empty_subsub":         1,
        "empty_description":    0
        }
        
    # Create the Banggood dictionary (source code 4 for EU product).
    xpath_dict['4_EU'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://eu.banggood.com",
        "query_url": "?currency=USD",
        "query_url_eu": "?language=en&country=150&currency=EUR",
        "na_url": "",
        "affiliate_link_before": "",
        # "affiliate_link_after": "?currency=USD?p=5!141510275320121293",
        "affiliate_link_after": "?p=5!141510275320121293&utm_source=bbs&utm_medium=CI&utm_content=zhangruihua",
        # (new arrivals).
        "product_list_item": "(//div[@class='box_content']/ul)[1]/li",
        "product_list_title": "div[2]/a",
        "product_list_url": "div[1]/a/@href",
        "next_page": "//div[@class='page_num']/a[position()=last()]/@href",
        "start_urls" : [
            "https://www.banggood.com/new-arrivals.html",
            ],
        "start_urls_eu" : [
            "https://eu.banggood.com/whtop-Eu-sellers-1091.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-140.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-1697.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-896.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-133.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-155.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-1031.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-274.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-892.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-1134.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-170.html?language=en&country=150&currency=EUR",
            "https://eu.banggood.com/whtop-Eu-sellers-1696.html?language=en&country=150&currency=EUR",       
            ],  
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.banggood.com/sitemap.html",
        "sitemap_link": "//div[@class='sitemap']/dl/dd/a[1]/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='pro_wrap box']",
        "title": "//h1/text()",
        "img_url": "(//div[@class='image_additional']/a/img/@data-normal)[1]", 
        "img_url2": "(//div[@class='image_additional']/a/img/@data-normal)[2]",
        "img_url3": "(//div[@class='image_additional']/a/img/@data-normal)[3]",        
        "list": "//b[@itemprop='price']/text()", #//div[@class='old']/@oriprice
        "price": "//b[@itemprop='price']/text()", #//div[@class='now']/@oriprice
        "stars": "//meta[@itemprop='ratingValue']/@content",
        "reviews": "//span[@itemprop='reviewCount']/text()",
        "sku": "//input[@id='sku']/@value",
        "stock": "normalize-space(//div[@class='status']/text())",
        "description": "normalize-space(//div[@class='good_tabs_box']/div[1])",  
        "cat": "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][2]/a/span/text()",
        "sub": "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][3]/a/span/text()",
        "subsub": "//ol[@typeof='BreadcrumbList']/li[@typeof='ListItem'][4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 1
        }
        
    # Create the Gearbest dictionary (source code 28).
    xpath_dict['28'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.gearbest.com",
        "query_url": "",
        "query_url_eu": "?currency=EUR",
        "na_url": "",
        "affiliate_link_before": "", #https://www.shareasale.com/r.cfm?u=761764&b=573201&m=52031&afftrack=CIsku&urllink=
        "affiliate_link_after": "?lkid=10490022", #CI SKU
        # (new arrivals).
        "product_list_item": "//ul[@id='catePageList']/li/div",
        "product_list_title": "p[@class='all_proNam']/a/@title",
        "product_list_url": "p[@class='all_proNam']/a/@href",
        "next_page": "//p[@class='listspan']/a[@class='next']/@href",
        "start_urls" : [
            "https://www.gearbest.com/new-products/?page_size=120",
            ],
        "start_urls_eu" : [
            "https://www.gearbest.com/warehouse/?wid=3&currency=EUR",
            "https://www.gearbest.com/warehouse/?wid=12&currency=EUR",
            "https://www.gearbest.com/warehouse/?wid=29&currency=EUR",
            "https://www.gearbest.com/warehouse/?wid=31&currency=EUR",
            ],         
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.gearbest.com/about/sitemap.html",
        "sitemap_link": "//div[@class='siteMapWrap']/dl/dd/a[1]/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='goods_info mb50']",
        "title": "//div[@class='goods_info_inner']/h1/text()",
        "img_url": "//div[@class='n_thumbImg_item']/ul/li[1]/a/img/@data-normal-img", 
        "img_url2": "//div[@class='n_thumbImg_item']/ul/li[2]/a/img/@data-normal-img",
        "img_url3": "//div[@class='n_thumbImg_item']/ul/li[3]/a/img/@data-normal-img",
        "list": "//span[@id='market_price']/@orgp",
        "price": "//input[@id='js_hidden_price']/@value",
        "stars": "//div[@class='g_review clearfix']/span[@itemprop='ratingValue']/text()",
        "reviews": "//strong[@itemprop='reviewCount']",
        "sku": "//div[@class='goods_info_inner']/span[2]/text()",
        "stock": "//button[@id='new_addcart']/text() | //a[@class='no_addToCartBtn']/text()", 
        "description": "//div[contains(@class, 'description')]/div[@class='product_pz']/node() | //div[contains(@class, 'description')]/div[@class='xxkkk']/node()",  # //div[contains(@class, 'product_pz_style2')]/node() | //div[contains(@class, 'mainfeatures')]/node()
        "cat": "//div[@class='bread-crumbs']/ol/li[2]/p/a/span/text()",
        "sub": "//div[@class='bread-crumbs']/ol/li[3]/p/a/span/text()",
        "subsub": "//div[@class='bread-crumbs']/ol/li[4]/p/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 1,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }
 
    # Create the Miniinthebox dictionary (source code 6).
    xpath_dict['6'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.miniinthebox.com",
        "query_url": "?currency=USD",
        "na_url": "http://www.miniinthebox.com/index.php?main_page=no_found&fname=Products",
        "affiliate_link_before": "https://ad.admitad.com/g/3aa22b4edb205609bfdc67b4bb3e03/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=570338&m=51900&afftrack=CIsku&urllink=
        "affiliate_link_after": "",    
        # (new arrivals).
        "product_list_item": "//div[@class='pagelet product-list']/div[@id='item-new']/dl",
        "product_list_title": "dd[@class='prod-name']/a/@title",
        "product_list_url": "dd[@class='prod-name']/a/@href",
        "next_page": "//li[@class='next']/a/@href",
        "start_urls" : [
            "http://www.miniinthebox.com/apple-accessories_c4861?sort=5d&newarrival=1", 
            "http://www.miniinthebox.com/jewelry-watches_c4676?sort=5d&newarrival=1",
            "http://www.miniinthebox.com/electronics-gadgets_c2624?sort=5d&newarrival=1",
            "http://www.miniinthebox.com/samsung-accessories_c5029?sort=5d&newarrival=1", 
            "http://www.miniinthebox.com/led-lighting_c4685?newarrival=1&sort=5d",
            "http://www.miniinthebox.com/sports-lifestyle_c8017?sort=5d&newarrival=1",
            "http://www.miniinthebox.com/computer-gadgets_c3017?sort=5d&newarrival=1",
            "http://www.miniinthebox.com/cell-phone-accessories_c3021?sort=5d&newarrival=1",
            "http://www.miniinthebox.com/household-pets_c3026?newarrival=1&sort=5d",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.miniinthebox.com/r/site-map.html",
        "sitemap_link": "//div[@class='widget w-siteMap']/div/ul/li/h3/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='container-main']",
        "title": "//div[@class='widget prod-info-title']/h1/text()",
        "img_url": "//ul[@class='list']/li[1]/a/img/@data-normal",
        "img_url2": "//ul[@class='list']/li[2]/a/img/@data-normal",
        "img_url3": "//ul[@class='list']/li[3]/a/img/@data-normal",
        "list": "//del[@class='del-price']/text()",
        "price": "//div[@class='current-price clearfix']/div/strong/text()",
        "stars": "//div[@class='widget prod-info-review ']/div/@class",
        "reviews": "//div[@class='widget prod-info-review ']/a/text()",
        "sku": "//span[@class='item-id']/text()",
        "stock": "//div[@class='order-actions']/input/@value | //div[@class='order-actions ']/input/@value",
        "description": "//div[contains(@class, 'prod-description-specifications')]/node()",  #//div[@id='prod-description-specifications']/div[@class='specTitle']/descendant::*/text()[normalize-space()]  | //h3[@class='empty']/text() | //div[@id='prod-description-specifications']/div[@class='bigTitle']/descendant::*/text()[normalize-space()]
        "cat": "normalize-space(//div[@id='breadcrumb']/ul/li[2]/dl/dt/a | //div[@id='breadcrumb']/ul/li[2]/a)",
        "sub": "normalize-space(//div[@id='breadcrumb']/ul/li[3]/dl/dt/a | //div[@id='breadcrumb']/ul/li[3]/a)", 
        "subsub": "normalize-space(//div[@id='breadcrumb']/ul/li[4]/dl/dt/a | //div[@id='breadcrumb']/ul/li[4]/a)",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 1
        } 

    # Create the LightInTheBox dictionary (source code 25).
    xpath_dict['25'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.lightinthebox.com/",
        "query_url": "?currency=USD",
        "na_url": "http://www.lightinthebox.com/index.php?main_page=no_found&fname=Products",
        "affiliate_link_before": "https://ad.admitad.com/g/383ee64557205609bfdc7d95a12660/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=570338&m=51900&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='pagelet product-list']/div[@id='item-new']/dl",
        "product_list_title": "dd[@class='prod-name']/a/@title",
        "product_list_url": "dd[@class='prod-name']/a/@href",
        "next_page": "//li[@class='next']/a/@href",
        "start_urls" : [
            "http://www.lightinthebox.com/c/weddings-events_1180?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/fashion_71?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/health-and-beauty_76?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/home-and-garden_75?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/shoes_3349?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/electronics_2619?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/premium-brands_42061?sort=5d&newarrival=1",
            "http://www.lightinthebox.com/c/beauty-hair_59321?sort=5d&newarrival=1"
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.lightinthebox.com/r/site-map.html",
        "sitemap_link": "//div[@class='widget w-siteMap']/div/ul/li/h3/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='container-main']",
        "title": "//div[@class='widget prod-info-title']/h1/text()",
        "img_url": "//ul[@class='list']/li[1]/a/img/@data-normal | //div[@class='list']/div[1]/img/@data-normal",
        "img_url2": "//ul[@class='list']/li[2]/a/img/@data-normal | //div[@class='list']/div[2]/img/@data-normal",
        "img_url3": "//ul[@class='list']/li[3]/a/img/@data-normal | //div[@class='list']/div[3]/img/@data-normal",
        "list": "//del[@class='del-price']/text()",
        "price": "//div[@class='current-price clearfix']/div/strong/text()",
        "stars": "//div[@class='widget prod-info-review ']/div/@class",
        "reviews": "//div[@class='widget prod-info-review ']/a/text()",
        "sku": "//span[@class='item-id']/text()",
        "stock": "//div[@class='order-actions']/input/@value | //div[@class='order-actions ']/input/@value",
        "description": "//div[contains(@class, 'prod-description-specifications')]/node()", # //div[@id='prod-description-specifications']/div[@class='specTitle']/descendant::*/text()[normalize-space()]  | //h3[@class='empty']/text() | //div[@id='prod-description-specifications']/div[@class='bigTitle']/descendant::*/text()[normalize-space()]
        "cat": "//div[@id='breadcrumb']/ul/li[2]/dl/dt/a/text() | //div[@id='breadcrumb']/ul/li[2]/a/text()",
        "sub": "//div[@id='breadcrumb']/ul/li[3]/dl/dt/a/text() | //div[@id='breadcrumb']/ul/li[3]/a/text()", 
        "subsub": "//div[@id='breadcrumb']/ul/li[4]/dl/dt/a/text() | //div[@id='breadcrumb']/ul/li[4]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }   
        
    # Create the Tmart dictionary (source code 7).
    xpath_dict['7'] = {
        # The following items are for the new URL list scraper
        "source_url":               "http://www.tmart.com",
        "query_url":                "",
        "na_url":                   "http://www.tmart.com/page_not_found",
        "affiliate_link_before":    "https://ad.admitad.com/g/h2i3nd0z0d205609bfdccb8cbcf449/?subid=CIsku&ulp=", # SAS Link: https://www.shareasale.com/r.cfm?u=761764&b=295027&m=31949&afftrack=CIsku&urllink=
        "affiliate_link_after":     "", #?aid=53419&utm_source=saff&utm_medium=referral&utm_campaign=self
        # (new arrivals).
        "product_list_item":        "//div[@class='na_list_m_box']",
        "product_list_title":       "span[@class='na_list_m_box_name']/a/@title",
        "product_list_url":         "span[@class='na_list_m_box_name']/a/@href",
        "next_page":                "(//li[@class='zc-next']/a/@href)[1]",
        "start_urls" : [
            "http://www.tmart.com/ShopWays/New-Arrivals.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":      "http://www.tmart.com/site_map.html",
        "sitemap_link":     "//li[@class='level2']/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":  "//div[contains(@class, 'J_prodcut_left')]",
        "title":            "//span[@class='J_ppname']/text()",
        "img_url":          "//div[@id='products_image_box']/ul/li[1]/a/img/@data-large",
        "img_url2":         "//div[@id='products_image_box']/ul/li[2]/a/img/@data-large",
        "img_url3":         "//div[@id='products_image_box']/ul/li[3]/a/img/@data-large",
        "list":             "//span[@class='J_pprice']/span[@class='font16 strong font-black line-through']/text()",
        "price":            "//span[@class='J_pprice']/span[@class='font36 strong font-light-red']/text()", 
        "stars":            "//span[@itemprop='ratingValue']",
        "reviews":          "//span[@itemprop='reviewCount']",
        "sku":              "translate(//span[contains(@class, 'J_pmodel')]/text(),'SKU:','')",
        "stock":            "//div[@class='add_cart_button_container']/a/text() | //button[contains(@class, 'J_addtocart')]/text()", 
        "description":      "//div[@id='description']/node()", #normalize-space(//div[@id='description']/text())
        "cat":              "//ul[@class='breadcrumb']/li[@class='dropdown'][1]/a/@title",
        "sub":              "//ul[@class='breadcrumb']/li[@class='dropdown'][2]/a/@title",
        "subsub":           "//ul[@class='breadcrumb']/li[@class='dropdown'][3]/a/@title",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }  

    # Create the FocalPrice dictionary (source code 5).
    xpath_dict['5'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.focalprice.com",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=134433&m=18404&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@id='list_content']/div",
        "product_list_title": "ul[@class='infobox']/li[@class='proName f11']/a/@title",
        "product_list_url": "ul[@class='infobox']/li[@class='proName f11']/a/@href",
        "next_page": "//a[@class='next']/@href",
        "start_urls" : [
            "http://www.focalprice.com/iphone-5c/ca-001023.html",
            # "http://dynamic.focalprice.com/new-arrivals?pagesize=72",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.focalprice.com/SiteMap",
        "sitemap_link": "//ul[@class='top_categories']/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='pro_detail']",
        "title": "//h1[@id='productName']/text()",
        "img_url": "//ul[@id='imgs']/li[1]/img/@jqimg",
        "img_url2": "//ul[@id='imgs']/li[2]/img/@jqimg",
        "img_url3": "//ul[@id='imgs']/li[3]/img/@jqimg",
        "list": "//s[@id='market_price']/text()", # Alternative 'number(substring(//s[@id='market_price']/text(), 5, 8))'
        "price": "concat(//span[@id='unit_price']//text(), //span[@id='unit_price']/sup/text())",
        "stars": "floor(translate(//span[@class='allrate']/@style, 'width:px;', '') div 14)",
        "reviews": "//em[@class='cf50']/text()",
        "sku": "//em[@id='sku']/text()",
        "stock": "//div[@class='ins_box']/p[@class='stock']/span[@id='shippingtime']/text()",  #NOT USED -> We request a XHR call -> http://dynamic.focalprice.com/QueryStockStatus?sku=HP3182B # OLD -> //p[@class='stock']/input[@id='stock_allowBuy']/@value
        "description": "//div[@id='summary']/text()",
        "cat": "//span[@class='snav_taq']/a[2]/text()",
        "sub": "//span[@class='snav_taq']/a[3]/text()",
        "subsub": "//span[@class='snav_taq']/a[4]/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }          
    
    # Create the TinyDeal dictionary (source code 20).
    xpath_dict['20'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.tinydeal.com",
        "query_url": "?currency=USD",
        "query_url_eu": "?currency=EUR&ship_to=NL", #?language=en&currency=EUR
        "na_url": "https://www.tinydeal.com/products_new.html",
        "affiliate_link_before": "https://ad.admitad.com/g/590bc151bb205609bfdc91a72d4870/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=612501&m=53769&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='p_box_wrapper']",
        "product_list_title": "li/a[@class='p_box_title']/text()",
        "product_list_url": "li/a[@class='p_box_title']/@href",
        "next_page": "//a[@class='nextPage']/@href",
        "start_urls" : [
            "https://www.tinydeal.com/products_new.html?recently_day=14&language=en&currency=USD",
            ],
        "start_urls_eu" : [
            "https://www.tinydeal.com/products_all.html?categories_id=1895&currency=EUR&language=en&ship_to=NL",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://help.tinydeal.com/site-map?currency=USD",
        "sitemap_link": "//div[@id='site_map']/div/div[@class='second']/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@id='product_main_header']",
        "title": "//h1[@id='productName']/text()",
        "img_url": "(//ul[@class='product_list_li_ul']/li[1]/img/@imgb)[1]",
        "img_url2": "(//ul[@class='product_list_li_ul']/li[2]/img/@imgb)[1]",
        "img_url3": "(//ul[@class='product_list_li_ul']/li[3]/img/@imgb)[1]",
        "list": "//span[@class='normalprice cen']/strong/text()",
        "price": "//span[@class='site-price']/span/text()",
        "stars": "//span[@itemprop='rating']/text() | //span[@title='No ratings']/text()",
        "reviews": "//p[@id='review_num']/a/span[@itemprop='count']/text() | //span[@class='g_reviews']/text()",
        "sku": "//form[@id='post_review']/input[@name='products_id']/@value", #Old: //div[@class='buy_now_area']/input[@name='products_id']/@value
        "stock": "//div[@class='fl products_qty_show']/text() | //span[@id='spanArrivalNotice'] | //div[@class='soldout-subscribe']/p/text()",
        "description": "(//ul[@class='features_ul']/li | //ul[@class='features_ul']/table/tbody/tr/td/div/div[1] | //ul[@class='features_ul']/table/tbody/tr/td/div/div[2] | //ul[@class='features_ul']/table/tbody/tr/td/div/div[3] | //ul[@class='features_ul']/li/table/tbody/tr/td/div/div[1] | //ul[@class='features_ul']/text() | //ul[@class='features_ul']/table/tbody/tr/td/div[1])[not(descendant::img)]",
        # "description": "//div[@id='productDescription']/div[not(contains(@class, 'invisible'))]/node()",
        "cat": "//div[@id='navBreadCrumb']/a[2]/text()",
        "sub": "//div[@id='navBreadCrumb']/a[3]/text()",
        "subsub": "//div[@id='navBreadCrumb']/a[4]/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 1,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 1
        }  

    # Create the Geekbuying dictionary (source code 31).
    xpath_dict['31'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.geekbuying.com/",
        "query_url": "?currency=USD",
        "query_url_eu": "?currency=EUR",
        "na_url": "http://www.geekbuying.com/Product/NotFoundProduct",
        "affiliate_link_before": "https://ad.admitad.com/g/78tuvzaw8k205609bfdc0267b86f6e/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=371154&m=38812&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//li[@class='searchResultItem']",
        "product_list_title": "div[@class='name']/a/@title",
        "product_list_url": "div[@class='name']/a/@href",
        "next_page": "//div[@id='pagination']/a[@class='next']/@href",
        "start_urls" : [
            "http://www.geekbuying.com/new-arrivals/0-15days/?sort=1",
            ],
        "start_urls_eu" : [
            "http://www.geekbuying.com/category/ES-Warehouse-1652/1-80-3-0-0-0-grid.html?currency=EUR",
            "http://www.geekbuying.com/category/UK-Warehouse-1303/1-80-3-0-0-0-grid.html?currency=EUR",
            "http://www.geekbuying.com/category/FR-Warehouse-1730/1-80-3-0-0-0-grid.html?currency=EUR",
            ],  
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.geekbuying.com/", # They dont have an html sitemap
        "sitemap_link": "//div[@id='leftnavigator']/ul/li/a/@href", # We just use the links on the main page
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@id='handleBuy']",
        "title": "normalize-space(//h1[@id='productName']/text())",   
        "img_url": "concat(substring(concat(substring-before(//ul[@id='thumbnail']/li[1]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[1]/a/img/@src, 'make_pic')),0 , string-length(concat(substring-before(//ul[@id='thumbnail']/li[1]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[1]/a/img/@src, 'make_pic'))) - 4), '.jpg')",
        "img_url2": "concat(substring(concat(substring-before(//ul[@id='thumbnail']/li[2]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[2]/a/img/@src, 'make_pic')),0 , string-length(concat(substring-before(//ul[@id='thumbnail']/li[2]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[2]/a/img/@src, 'make_pic'))) - 4), '.jpg')",
        "img_url3": "concat(substring(concat(substring-before(//ul[@id='thumbnail']/li[3]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[3]/a/img/@src, 'make_pic')),0 , string-length(concat(substring-before(//ul[@id='thumbnail']/li[3]/a/img/@src, 'make_pic'), 'ggo_pic', substring-after(//ul[@id='thumbnail']/li[3]/a/img/@src, 'make_pic'))) - 4), '.jpg')",
        "list": "normalize-space(//span[@id='regprice']/text())",
        "price": "//span[@id='saleprice']/text()",
        "stars": "//span[@itemprop='ratingValue']/@title",
        "reviews": "//span[@itemprop='reviewCount']/a/text()",
        "sku": "//span[@id='iconCodeDiv1']/b/text()",
        "stock": "//div[@id='numberDiv']/div[@class='buyItNow2013']/text() | //a[@class='noticestockLink']/text() | //a[@class='SoldOutLink']/text()",
        # "description": "//div[@id='DESCRIPTION_HTML']/div[@id='Description']/*[preceding-sibling::h2='Highlights' and following-sibling::h2='Specification'][not(descendant::img)] | //div[@id='DESCRIPTION_HTML']/descendant::p/text()[not(descendant::img)]", #//div[@id="DESCRIPTION_HTML"]/node()
        "description": "//div[@id='DESCRIPTION_HTML']/node()[2]",
        "cat": "//ul[@id='crumbs']/li[2]/div/div/a/text() | //ul[@id='crumbs']/li[2]/a/text()",
        "sub": "//ul[@id='crumbs']/li[3]/div/div/a/text() | //ul[@id='crumbs']/li[3]/a/text()",
        "subsub": "//ul[@id='crumbs']/li[4]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 1
        }  

       
    # Create the Dealsmachine dictionary (source code 19). 
    xpath_dict['19'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.dealsmachine.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=284314&m=31237&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//ul[@class='p_listBox clearfix']/li",
        "product_list_title": "p[@class='p_name pt10']/a/@title",
        "product_list_url": "p[@class='p_name pt10']/a/@href",
        "next_page": "(//p[@class='listspan']/a[contains(text(),'Next')]/@href)[1]",
        "start_urls" : [
            "http://www.dealsmachine.com/new-arrivals/",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.dealsmachine.com/sitemap-index.html",
        "sitemap_link": "//div[@id='sitemap']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@id='mainWarp']/div[1]",
        "title": "normalize-space(//h1/text())",
        "img_url": "//div[@class='items']/ul/li[1]/a/img/@bigimg",
        "img_url2": "//div[@class='items']/ul/li[2]/a/img/@bigimg",
        "img_url3": "//div[@class='items']/ul/li[3]/a/img/@bigimg",
        "list": "//table/tbody/tr[2]/td[2]/span[@class='my_shop_price']/text()",
        "price": "//span[@id='pk0']/text() | //span[@id='unit_price']/@orgp[last()]", #//table/tbody/tr[2]/td[2]/span[@class='spanred1']/span[@class='my_shop_price']/text()
        "stars": "//p[@class='proMain_writeReview']/text()", #Not always available - substring(//p[@class='proMain_writeReview']/text(),1,1)
        "reviews": "//p[@class='proMain_writeReview']/a[@class='reviewNum']/text()",
        "sku": "//div[@class='proMain_info clearfix']/em/text()",
        "stock": "//div[@class='proMain_status']/span[1]/text()",
        "description": "//div[contains(@class, 'MainInfo_showBox')][1]/div/div[@class='xxkkk2']/node()", #//div[@class='xxkkk2']/text() | //table[contains(@class,'3')][1][descendant::*/text() and not(//div[@class='xxkkk2']/text())][1]
        "cat": "//div[@class='fl curPath']/span[2]/a/span/text()",
        "sub": "//div[@class='fl curPath']/span[3]/a/span/text()",
        "subsub": "//div[@class='fl curPath']/span[4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 1
        }
    
    # Create the Newfrog dictionary (source code 29). 
    xpath_dict['29'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.newfrog.com/",
        "query_url": "?currency=USD", 
        "na_url": "",
        "affiliate_link_before": "https://ad.admitad.com/g/enfyv9i7oe205609bfdccc4476038e/?subid=CIsku&ulp=", #https://www.shareasale.com/r.cfm?u=761764&b=471054&m=46666&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//li[contains(@class, 'product-item')]/div[@class='product-item-info']",
        "product_list_title": "div[contains(@class, 'product-item-details')]/strong/a/text()",
        "product_list_url": "div[contains(@class, 'product-item-details')]/strong/a/@href",
        "next_page": "//li[contains(@class, 'pages-item-next')]/a/@href",
        "start_urls" : [
            "https://www.newfrog.com/new-arrivals.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.newfrog.com/sitemap.html",
        "sitemap_link": "//li[@class='cat']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='product-info-main']",
        "title": "//h1[@class='page-title']/span/text()",
        "img_url": "translate(substring-before(substring-after(//script[@type='text/x-magento-init'][contains(text(), 'img')], '\"img\":\"'), '\",'), '\\', '')", 
        "img_url2": "translate(substring-before(substring-after( substring-after(//script[@type='text/x-magento-init'][contains(text(), 'img')], '\"img\":\"'), '\"img\":\"'), '\",'), '\\', '')",
        "img_url3": "translate(substring-before(substring-after( substring-after( substring-after(//script[@type='text/x-magento-init'][contains(text(), 'img')], '\"img\":\"'), '\"img\":\"'), '\"img\":\"'), '\",'), '\\', '')",
        "list": "//div[@class='product-info-price']/div/span[contains(@class, 'old-price')]/span/span/span[@class='price']",
        "price": "//div[@class='product-info-price']/div/span[contains(@class, 'orange')]/span/span/span[@class='price']",
        "stars": "translate(//div[@class='rating-result']/span/span, '%', '') div 20",
        "reviews": "//div[@class='reviews-actions']/a/text()",
        "sku": "//div[@class='product-info-stock-sku']/div/div[@itemprop='sku']/text()",
        "stock": "substring-after(//div[@class='product-shippinginfo'], 'Delivery:')",
        "description": "//div[@id='product.info.description']/node()",
        "cat": "//div[@class='breadcrumbs']/ul/li[contains(@class, 'category')][1]/a/text()",
        "sub": "//div[@class='breadcrumbs']/ul/li[contains(@class, 'category')][2]/a/text()",
        "subsub": "//div[@class='breadcrumbs']/ul/li[contains(@class, 'category')][3]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 1,
        "empty_sub": 1,
        "empty_subsub": 1,
        "empty_description": 0
        }
        
    # Create the TomTop  dictionary (source code 15).
    xpath_dict['15'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.tomtop.com/",
        "query_url": "",
        "query_url_eu": "?currency=EUR",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=237912&m=27868&afftrack=CIsku&urllink=",
        "affiliate_link_after": "?aid=compare",
        # (new arrivals).
        "product_list_item": "//div[@class='productClass']",
        "product_list_title": "a[@class='productTitle']/@title",
        "product_list_url": "a[@class='productTitle']/@href",
        "next_page": "//li[@class='lineBlock pageN pageClick']/a/@href",
        "start_urls" : [
            "https://www.tomtop.com/new-arrivals/",
            ],
        "start_urls_eu" : [
            "https://www.tomtop.com/storage/uk/?currency=EUR&Warehouse=UK",
            "https://www.tomtop.com/storage/de/?currency=EUR&Warehouse=DE",
            "https://www.tomtop.com/storage/fr/?currency=EUR&Warehouse=FR",
            ],  
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.tomtop.com/sitemap.html",
        "sitemap_link": "//div[@class='site_map']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//section[@class='contentInside lbBox']",
        "title": "//h1/span[@itemprop='name']/text()",
        "img_url": "//ul[@class='productSmallmove lbBox moveBox']/li[1]/a/@href",
        "img_url2": "//ul[@class='productSmallmove lbBox moveBox']/li[2]/a/@href",
        "img_url3": "//ul[@class='productSmallmove lbBox moveBox']/li[3]/a/@href",
        "list": "substring-after(substring-before(//body/script[contains(text(),'price')], 'saleprice'), 'price')",
        "price": "//span[@class='fz_orange pricelab']/text()[1]", #//p[@id='detailPrice']
        "stars": "//span[@itemprop='ratingValue']",
        "reviews": "//span[@itemprop='reviewCount']",
        "sku": "//div[@class='toCart']/input[@id='productSku']/@value",
        "stock": "//meta[@itemprop='availability']/@content", #In Stock
        "description": "//div[@id='description']/node()", # //div[@id='description']/text()[normalize-space()][not(descendant::img)] | //div[@id='description']/descendant::p/text()[normalize-space()][1] | //div[@id='description']/descendant::span/text()[normalize-space()][1] | //div[@id='description']/descendant::div/text()[normalize-space()][1]
        "cat": "//ul[@typeof='BreadcrumbList']/li[@property='itemListElement'][2]/a/span/text()",
        "sub": "//ul[@typeof='BreadcrumbList']/li[@property='itemListElement'][3]/a/span/text()",
        "subsub": "//ul[@typeof='BreadcrumbList']/li[@property='itemListElement'][4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }
        
    # Create the Fasttech  dictionary (source code 22).    
    xpath_dict['22'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.fasttech.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=437122&m=44775&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='ProductGridItem']/div[@class='GridItemDesc']",
        "product_list_title": "div[@class='GridItemName']/a/text()",
        "product_list_url": "div[@class='GridItemName']/a/@href",
        "next_page": "(//span[@class='ControlArrows '][2]/a/@href)[1]",
        "start_urls" : [
            "https://www.fasttech.com/category/1/new-products",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.fasttech.com/pages/site-map",
        "sitemap_link": "//div[@id='StaticPageContent']/div/div/div/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//table[@class='TightTable']",
        "title": "//span[@id='content_ProductTitle']/text()",
        "img_url": "//div[@id='ThumbnailsPanel']/a[1]/@href",
        "img_url2": "//div[@id='ThumbnailsPanel']/a[2]/@href",
        "img_url3": "//div[@id='ThumbnailsPanel']/a[3]/@href",
        "list": "//span[@id='list_Price']", # Does Never Exist
        "price": "//meta[@itemprop='price']/@content",
        "stars": "//span[@itemprop='ratingValue']",
        "reviews": "//span[@itemprop='reviewCount']",
        "sku": "//meta[@itemprop='sku']/@content",
        "stock": "//meta[@itemprop='availability']/@content",
        "description": "//table[@class='AttributesTable'] | //div[@class='ProductDescriptions']", #normalize-space(//div[@class='ProductDescriptions'])  
        "cat": "//div[@class='Breadcrumb']/span[2]/a/span/text()",
        "sub": "//div[@class='Breadcrumb']/span[3]/a/span/text()",
        "subsub": "//div[@class='Breadcrumb']/span[4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }

    # Create the ChinaVasion dictionary (source code 9).  
    xpath_dict['9'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.chinavasion.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://ad.admitad.com/g/9kw3wjmepx205609bfdcfe9097859d/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=139417&m=18925&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='product_tile short']",
        "product_list_title": "a/span[@class='product_tile_font_s']/text()",
        "product_list_url": "a/@href",
        "next_page": "(//span[@class='arrow']/a[@rel='next']/@href)[1]",
        "start_urls" : [
            "https://www.chinavasion.com/products_new.php",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.chinavasion.com/sitemap/",
        "sitemap_link": "//a[@class='pcategories']/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@id='prod_falme']",
        "title": "//h1[@itemprop='name']/text()",
        "img_url": "concat('http:', substring-before((//div[@id='xys']/img[1]/@src), 'thumb_'), 'thumb_600x600.jpg')",
        "img_url2": "concat('http:', substring-before((//div[@id='xys']/img[2]/@src), 'thumb_'), 'thumb_600x600.jpg')",
        "img_url3": "concat('http:', substring-before((//div[@id='xys']/img[3]/@src), 'thumb_'), 'thumb_600x600.jpg')",
        "list": "//span[@class='discount']/span[1]/span[@class='ccy']/text()",
        "price": "//span[@id='current_price_div'] | //div[@id='prod_float']/div/span[@class='discount']/span[@class='ccy'][1]",   # //div[@itemprop='offers']/meta[@itemprop='price']/@content
        "stars": "//div[@class='item vcard']/div[2]/img/@class",
        "reviews": "//div[@class='item vcard']/div[2]/em/span",
        "sku": "//div[@class='item vcard']/p[@class='prod_model']/span[@class='code']/text() | //div[@class='item vcard']/span[@class='code']/text()",
        "stock": "//div[@itemprop='offers']/meta[@itemprop='availability']/@content | //div[@class='box_white']/p/strong/span/text()",
        "description": "//div[@itemprop='description']/text()",
        "cat": "//div[@id='breadcrumb']/span[2]/a/span/text()",
        "sub": "//div[@id='breadcrumb']/span[3]/a/span/text()",
        "subsub": "//div[@id='breadcrumb']/span[4]/a/span",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }        
    
    
    # Create the TVC-Mall dictionary (source code 30). 
    xpath_dict['30'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.tvc-mall.com",
        "query_url": "",
        "na_url": "https://www.tvc-mall.com/404.html",
        "affiliate_link_before": "https://ad.admitad.com/g/ypbc0wv2ou205609bfdc5e1d7c1983/?subid=CIsku&ulp=", #https://www.shareasale.com/r.cfm?u=761764&b=520357&m=49619&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='p-info']",
        "product_list_title": "div[@class='pro-title']/a/@title",
        "product_list_url": "div[@class='pro-title']/a/@href",
        "next_page": "//ul[@class='pagination pagination-sm']/li[last()]/a/@href",
        "start_urls" : [
            "https://www.tvc-mall.com/NewArrivals",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.tvc-mall.com/SiteMap",
        "sitemap_link": "//div[@class='phoneItem']/dl/dt/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='p-property']",
        "title": "//h1[@itemprop='name']/text()",
        "img_url": "//div[@class='images-block']/div[1]/a/img/@src",
        "img_url2": "//div[@class='images-block']/div[2]/a/img/@src",
        "img_url3": "//div[@class='images-block']/div[3]/a/img/@src",
        "list": "(//div[@class='price-info']/del[@class='old-price']/text())[1]",
        "price": "//div[@class='detail-item']/meta[@itemprop='price']/@content",
        "stars": "(translate(substring-after(//div[@class='star-img-big']/span/@style, 'width:'), '%','') div 20)",
        "reviews": "translate(//span[@class='rev-num']/text(), 'abcdefghijklmnopqrstuvwxyz()', '')",
        "sku": "//meta[@itemprop='sku']/@content",
        "stock": "//div[@class='detail-item']/meta[@itemprop='availability']/@content",
        "description": "//div[@class='system-description']/p/text() | //div[@class='system-description']/ul/li/p/text() | //div[@class='system-description']/ul/li/text()",
        "cat": "//div[@class='location']/ol/li[3]/a/text()",
        "sub": "//div[@class='location']/ol/li[4]/a/text()",
        "subsub": "//div[@class='location']/ol/li[5]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }

    # Create the Antelife dictionary (source code 63). 
    xpath_dict['63'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.antelife.com",
        "query_url": "",
        "query_url_eu": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=638410&m=54966&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//li[contains(@class,'item')]",  #//div[@class='grid-block']/ul/li
        "product_list_title": "div/h2/a/@title",
        "product_list_url": "div/h2/a/@href",
        "product_list_url_eu": "substring-before(substring-after(//script[contains(.,'url_code_EUR')], concat('var url_code_EUR = ', \"'\")), concat(\"'\",';'))",
        "next_page": "(//li[@class='next-icon']/a/@href)[1]",
        "start_urls" : [
            "http://www.antelife.com/mobile-phones.html?dir=desc&order=created_at",
            "http://www.antelife.com/mobile-accessories.html?dir=desc&order=created_at",
            "http://www.antelife.com/phone-accessories-1.html?dir=desc&order=created_at",
            "http://www.antelife.com/electronic-gadgets.html?dir=desc&order=created_at",
            "http://www.antelife.com/computer-networking.html?dir=desc&order=created_at",
            "http://www.antelife.com/electronic-gadgets/smart-electronic/smart-wearable.html",
            "http://www.antelife.com/car-electronics.html?dir=desc&order=created_at",
            ],
        "start_urls_eu" : [
            "http://www.antelife.com/newspainwarehouse.html",
            "http://www.antelife.com/germanywarehouse.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.antelife.com/site-map",
        "sitemap_link": "//div[@class='sitemap_tit_list']/ul/li/dl/dd/p/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='product-essential']",
        "title": "//h1[@itemprop='name']/text()",
        "img_url": "//meta[@property='og:image']/@content", 
        "img_url2": "(//ul[@id='mycarousel']/li/img/@middlename)[2]",
        "img_url3": "(//ul[@id='mycarousel']/li/img/@middlename)[3]",
        "list": "//span[@class='old-price']",
        "price": "//div[@class='product-name']/div/span[@itemprop='price']/text()", #//div[@class='price-cartbg']/div/p[contains(@class, 'my-p-info-final')]/span[@class='price']
        "stars": "//div[@class='ratings']/span[@itemprop='ratingValue']",
        "reviews": "translate(//div[@class='ratings']/span[@itemprop='reviewCount'], ' reviews', '')",
        "sku": "substring-after(//span[@class='p-sku'], 'SKU: ')",
        "stock": "//div[@class='price-cartbg']/div/p[1]/span[2]/text()",
        "description": "normalize-space(//div[contains(@class, 'box-description')]/div[@class='std'])",
        "cat": "translate(normalize-space(//div[@class='breadcrumbs']/ul/li[contains(@class ,'category')][1]), '>', '')",
        "sub": "translate(normalize-space(//div[@class='breadcrumbs']/ul/li[contains(@class ,'category')][2]), '>', '')",
        "subsub": "translate(normalize-space(//div[@class='breadcrumbs']/ul/li[contains(@class ,'category')][3]), '>', '')",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 1,
        "empty_cat": 1,
        "empty_sub": 1,
        "empty_subsub": 1,
        "empty_description": 0
        }

        
    # Create the Cafago dictionary (source code 64). 
    xpath_dict['64'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.cafago.com",
        "query_url":                "?currency=USD",
        "query_url_eu":             "?currency=EUR",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/xrzqqr83az205609bfdc0789458fbf/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=945079&m=68967&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item": "//ul[@class='lbBox categoryProductList']/li",
        "product_list_title": "div[@class='productClass']/a[@class='productTitle']/@title",
        "product_list_url": "div[@class='productClass']/a[@class='productTitle']/@href",
        "next_page": "//ul[@class='lbBox pagingWarp']/li[contains(@class, 'pageN')]/a/@href",
        "start_urls" : [
            "https://www.cafago.com/en/new-arrivals/?currency=USD",
            ],
        "start_urls_eu" : [
            "https://www.cafago.com/en/storage/de/?currency=EUR&Warehouse=DE",
            "https://www.cafago.com/en/storage/uk/?currency=EUR&Warehouse=UK",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.cafago.com/en/sitemap.html",
        "sitemap_link": "//div[@class='site_map']/h2/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@itemtype='http://schema.org/Product']",
        "title": "//h1/span[@itemprop='name']/text()",
        "img_url": "//div[contains(@class, 'productSmallPic')]/ul/li[1]/a/@href",
        "img_url2": "//div[contains(@class, 'productSmallPic')]/ul/li[2]/a/@href",
        "img_url3": "//div[contains(@class, 'productSmallPic')]/ul/li[3]/a/@href",
        "list": "substring-before(substring-after(//script[contains(.,'var product')],'\"price\":'), ',')", # //div[@class='saleWarp']/p/span
        "price": "substring-before(substring-after(//script[contains(.,'var product')],'\"saleprice\":'), ',')",  #//p[@id='detailPrice']/text()
        "stars": "//span[@itemprop='ratingValue']",
        "reviews": "//span[@itemprop='reviewCount']",
        "sku": "//h1/span[@id='p_sku_s']/@data-sku",
        "stock": "//input[@id='productStatus']/@value",
        "description": "//div[@id='description']/node()", #normalize-space(//div[@id='description']/text())
        "cat": "(//ul[@typeof='BreadcrumbList']/li/a/@title)[2]",
        "sub": "(//ul[@typeof='BreadcrumbList']/li/a/@title)[3]",
        "subsub": "(//ul[@typeof='BreadcrumbList']/li/a/@title)[4]",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }

    
    # Create the DinoDirect dictionary (source code 8). 
    xpath_dict['8'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.dinodirect.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=724218&m=59043&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//ul[@class='product_list']/li",
        "product_list_title": "div[@class='bt_dp_name']/a/@title",
        "product_list_url": "div[@class='bt_dp_name']/a/@href",
        "next_page": "(//div[contains(@class, 'about_pages')]/a/@href)[last()]",
        "start_urls" : [
            "http://www.dinodirect.com/shopways/New-Arrivals/",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.dinodirect.com/sitemap.html",
        "sitemap_link": "//div[@class='sitemap_tit_list']/ul/li/dl/dt/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='bt_sp_info_show']",
        "title": "//h1[@itemprop='name']/text()",
        "img_url": "//div[contains(@class, 'newProductShowImg')]/ul/li[2]/input[1]/@value",
        "img_url2": "//div[contains(@class, 'newProductShowImg')]/ul/li[3]/input[1]/@value",
        "img_url3": "//div[contains(@class, 'newProductShowImg')]/ul/li[4]/input[1]/@value",
        "list": "//span[@id='productoldprice']/text()",
        "price": "//span[@id='productcurprice']/text()",
        "stars": "//div[@itemprop='aggregateRating']/span[@class='Value']",
        "reviews": "//div[@itemprop='aggregateRating']/span[@class='count']",
        "sku": "substring-after(//div[@itemprop='aggregateRating']/div/label[@class='gray'], 'SKU: ')",
        "stock": "//div[@id='AddToCartBn']/input[@type='submit']/@class",
        "description": "//li[@style='word-wrap:break-word;'] | //li[@class='property-item'] | //span[@style='font-size: 16.0px;'] | //span[@style='font-size: 13.0px;']",
        "cat": "//div[@class='det_sc']/div/ul/li[2]/div/div/a/@title",
        "sub": "//div[@class='det_sc']/div/ul/li[3]/div/div/a/@title",
        "subsub": "//div[@class='det_sc']/div/ul/li[4]/a/@title",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 0,
        "empty_description": 0
        }
        
        
        
    
    # Create the ChinaBuye dictionary (source code 10).         
    xpath_dict['10'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.chinabuye.com",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=206913&m=25270&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//td[@class='pro_list_name']",
        "product_list_title": "h5/a/@title",
        "product_list_url": "h5/a/@href",
        "next_page": "(//a[@class='tool_next']/@href)[last()]",
        "start_urls" : [
            "http://www.chinabuye.com/new-arrival?limit=84",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "http://www.chinabuye.com/catalog/seo_sitemap/category/?p=1",
        "sitemap_link": "//li[@class='level-1']/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='padder']",
        "title": "//h1[@class='product-name']/text()",
        "img_url": "concat(substring-before(//div[@class='more_views_main']/ul/li[1]/a/img/@src, 'thumbnail/70x70/'), 'image/' ,substring-after(//div[@class='more_views_main']/ul/li[1]/a/img/@src, 'thumbnail/70x70/') )",
        "img_url2": "concat(substring-before(//div[@class='more_views_main']/ul/li[2]/a/img/@src, 'thumbnail/70x70/'), 'image/' ,substring-after(//div[@class='more_views_main']/ul/li[2]/a/img/@src, 'thumbnail/70x70/') )",
        "img_url3": "concat(substring-before(//div[@class='more_views_main']/ul/li[3]/a/img/@src, 'thumbnail/70x70/'), 'image/' ,substring-after(//div[@class='more_views_main']/ul/li[3]/a/img/@src, 'thumbnail/70x70/') )",
        "list": "substring-after(substring-before(//script[contains(. , 'var optionsPrice')], ',\"skipCalculate'), 'productOldPrice\":')",
        "price": "substring-after(substring-before(//script[contains(. , 'var optionsPrice')], ',\"productOldPrice'), 'productPrice\":')",
        "stars": "translate(substring-after(//div[@class='product-info-box']/div/div/div[@class='rating']/@style, 'width:'), '%', '') div 20",
        "reviews": "substring-before(//div[@class='product-info-box']/div/a[1]/text(), ' Review(s)')",
        "sku": "substring-after(//div[@class='product-info-box']/div/span[@class='regular-price']/@id | //div[@class='product-info-box']/div/p[@class='special-price']/span[@class='price']/@id, 'product-price-')",
        "stock": "(//div[@class='product-info-box']/p)[last()]",
        "description": "//div[@id='productdes']/node()[not(self::table | descendant::table | child::table)]", # //div[@id='productdes']/descendant::*[normalize-space(text())]
        "cat": "//ul[@class='breadcrumbs']/li[3]/a/text()",
        "sub": "//ul[@class='breadcrumbs']/li[5]/a/text()",
        "subsub": "//ul[@class='breadcrumbs']/li[7]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 1,
        "empty_subsub": 1,
        "empty_description": 0
        }
      
    
    # Create the Sunsky-Online dictionary (source code 21).    
    xpath_dict['21'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.sunsky-online.com/",
        "query_url": "",
        "na_url": "https://www.sunsky-online.com/base/info!pageNotFound.do",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=659059&m=55818&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='shopcart_cont']/ul/li",
        "product_list_title": "a/@title",
        "product_list_url": "a/@href",
        "next_page": "concat('?page=', number((//div[@class='paginationLinks']/input/@value)[last()]) + 1)",
        "start_urls" : [
            "https://www.sunsky-online.com/marketing/promotion!newArrivals.do",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.sunsky-online.com/base/info!siteMap.do",
        "sitemap_link": "//div[@class='sitemap']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[contains('class', productBox)]",
        "title": "substring-after(//title, 'SUNSKY - ')",
        "img_url": "//img[@id='mainImg']/@src | (//ul[@id='picCtn']/li/a/img/@src)[1]", #If One Image take the main one
        "img_url2": "(//ul[@id='picCtn']/li/a/img/@src)[2]",
        "img_url3": "(//ul[@id='picCtn']/li/a/img/@src)[3]",
        "list": "//tr[@class='curr_price'][1]/td/span/text()",
        "price": "//tr[@class='curr_price'][1]/td/span/text()",
        "stars": "//b[.='Praise Degree']/following-sibling::div/text()",
        "reviews": "//a[@href='#reviews']/text()",
        "sku": "//div[@class='itemDiv']/b/text()",
        "stock": "//td/input[@class='a_arrnot']/@rel | //h2/span/text()",
        "description": "//h3[.='Description']/following-sibling::div/div[1]/node()", # //h3[.='Description']/following-sibling::div/div[1]
        "cat": "(//div[@class='breadCrumb']/a/text())[2]",
        "sub": "(//div[@class='breadCrumb']/a/text())[3]",
        "subsub": "(//div[@class='breadCrumb']/a/text())[4]",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }

        
    # Create the CNDirect dictionary (source code 65). 
    xpath_dict['65'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.cndirect.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/q4gsldoiz4205609bfdc9fecbe62c5/?subid=CIsku&ulp=", #https://www.shareasale.com/r.cfm?u=761764&b=515794&m=49411&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//div[@class='search_result_detail']",
        "product_list_title":       "div[@class='item_description']/a/@title",
        "product_list_url":         "div[@class='item_description']/a/@href",
        "next_page":                "(//div[@class='pages']/div/a[@class='next']/@href)[last()]",
        "start_urls" : [
            "https://www.cndirect.com/product-whatsnew.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":              "https://www.cndirect.com/",
        "sitemap_link":             "//div[@class='first_category']/a[@class='nav_link']/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":          "//div[contains(@class,'product_content')]",
        "title":                    "//h1[@class='prodetail_title']/text()",
        "img_url":                  "//div[@id='product_img_zoom']/img/@src",
        "img_url2":                 "//div[@id='spec-list']/ul/li[2]/@chuimg",
        "img_url3":                 "//div[@id='spec-list']/ul/li[3]/@chuimg",
        "list":                     "//div[@class='prodetail_price']/div[@class='item_old_price']/font[@class='currency_price']/@data-usd_val",
        "price":                    "//div[@class='prodetail_price']/div[@class='item_current_price']/font[@class='currency_price']/@data-usd_val",
        "stars":                    "//div[@class='review_number']/a/span",
        "reviews":                  "substring-after(substring-before(//div[@class='review_number']/a[2], 'review'), '(')",
        "sku":                      "//span[@class='sku']/@spu",
        "stock":                    "//a[contains(@class, 'cart_button')]",
        "description":              "substring-before(substring-after(//script[@type='application/ld+json'], 'description\" : \"'), '\",')", #//div[@class='prodetail_info_nr_list']/*[following-sibling::p]
        # "description":              "//div[@class='prodetail_info_nr_list']/*[following-sibling::p]", 
        "cat":                      "//div[@class='path']/a[2]/h2/text()", 
        "sub":                      "//div[@class='path']/a[3]/h2/text()", 
        "subsub":                   "//div[@class='path']/a[4]/h2/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars":          1, 
        "empty_reviews":        1,
        "empty_stock":          0,
        "empty_list":           1,
        "empty_cat":            0,
        "empty_sub":            0,
        "empty_subsub":         1,
        "empty_description":    0
        }
        
    # Create the Zapals dictionary (source code 66).
    xpath_dict['66'] = {
        # The following items are for the new URL list scraper
        "source_url": "https://www.zapals.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://ad.admitad.com/g/kp9wo7ln06205609bfdce6f36fde24/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=872901&m=66110&afftrack=CIsku&urllink=
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='hru-content']",
        "product_list_title": "div/a/div/text()",
        "product_list_url": "div/a/@href",
        "next_page": "(//a[@class='next ']/@href)[last()]",
        "start_urls" : [
            "https://www.zapals.com/new-arrivals.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "https://www.zapals.com/sitemap.html",
        "sitemap_link": "//div[@class='sitemap']/dl[not(@class='other-link')]/dd/a[1]/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[@class='product-essential']",
        "title": "//h1[@class='product-name']/text()",
        "img_url": "//div[@class='more-images']/div/ul/li[1]/a/@href",
        "img_url2": "//div[@class='more-images']/div/ul/li[2]/a/@href",
        "img_url3": "//div[@class='more-images']/div/ul/li[3]/a/@href",
        "list": "//div[@class='product-shop']/div[@class='price-box']/span[@class='old-price']/span/text()",
        "price": "//div[@class='product-shop']/div[@class='price-box']/span[@class='special-price']/span/span[@itemprop='price']/@content",
        "stars": "//span[@itemprop='ratingValue']",
        "reviews": "//span[@itemprop='reviewCount']",
        "sku": "substring-after(//div[@class='product-review'][2], 'SKU: ')",
        "stock": "//p[contains(@class, 'availability')]/span/text()",
        "description": "//div[@class='std product-features']/div/node() | //div[@class='std product-features']/node() [1]", #//div[@class='std product-features']/div//*[not(self::table or self::img or self::a or self::CDATA or self::script or self::h3)]
        "cat": "//ol[@itemprop='breadcrumb']/li[2]/a/span/text()",
        "sub": "//ol[@itemprop='breadcrumb']/li[3]/a/span/text()",
        "subsub": "//ol[@itemprop='breadcrumb']/li[4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 1,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 1,
        "empty_sub": 1,
        "empty_subsub": 1,
        "empty_description": 0
        }
    
    """
    # Create the Rosewholesale dictionary (source code 57).
    xpath_dict['57'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.rosewholesale.com/",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "",
        "product_list_title": "",
        "product_list_url": "",
        "next_page": "",
        "start_urls" : [
            "http://www.rosewholesale.com/new/?pz=200",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "",
        "sitemap_link": "",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "",
        "title": "",
        "img_url": "",
        "img_url2": "",
        "img_url3": "",
        "list": "",
        "price": "",
        "stars": "",
        "reviews": "",
        "sku": "",
        "stock": "",
        "description": "",
        "cat": "",
        "sub": "",
        "subsub": "",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 0,
        "empty_description": 0
        }
    """    
        
    # Create the SheIn dictionary (source code 59).
    xpath_dict['59'] = {
        # The following items are for the new URL list scraper
        "source_url":               "http://www.shein.com",
        "query_url":                "?ref=us",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/1kjlqr06u0205609bfdcf0af71e07a/?subid=CIsku&ulp=", #https://www.shareasale.com/r.cfm?u=761764&b=374756&m=39236&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//div[contains(@class, 'prd-ct-gd-item')]",
        "product_list_title":       "div/div[@class='description']/a/@title",
        "product_list_url":         "div/div[@class='description']/a/@href",
        "next_page":                "//a[@class='she-active']/@href",
        "start_urls" : [
            "http://www.shein.com/daily-new.html?ref=us",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":          "http://www.shein.com",
        "sitemap_link":         "//div[contains(@class, 'second-link')]/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":      "//div[@class='m-productd']",
        "title":                "//h2[@class='name']/text()",
        "img_url":              "//div[contains(@class, 'thumbs-wrapper')]/div[1]/div/img/@src",
        "img_url2":             "//div[contains(@class, 'thumbs-wrapper')]/div[2]/div/img/@src",
        "img_url3":             "//div[contains(@class, 'thumbs-wrapper')]/div[3]/div/img/@src",
        "list":                 "//div[@id='shop_price_u']/@price",
        "price":                "substring-before(substring-after(//script[@type='application/ld+json'], 'price\": \"'), '\",')",
        "stars":                "//div[@class='rating-ctn']/div/span/text()",
        "reviews":              "//div[@class='custom-reviews']/h3/span/text()",
        "sku":                  "//div[@class='summary']/span[@class='sku']/span[@id='productCodeSpan']/text()",
        "stock":                "//div[contains(@class, 'detail-submit-btn')]/div[contains(@class, 'she-btn-black')]/text() | //div[contains(@class, 'detail-submit-btn')]/div[contains(@class, 'she-btn-black')]/div[contains(@id, 'addto_')]",
        "description":          "//div[@class='description-con goods_description_con']/node()",
        "cat":                  "//ul[@class='she-breadcrumb']/li[2]/a/@title | //ul[@class='she-breadcrumb']/li[2]/div[@class='dropdown-title']/span/a/@title",
        "sub":                  "//ul[@class='she-breadcrumb']/li[3]/a/@title | //ul[@class='she-breadcrumb']/li[3]/div[@class='dropdown-title']/span/a/@title",
        "subsub":               "//ul[@class='she-breadcrumb']/li[4]/a/@title | //ul[@class='she-breadcrumb']/li[4]/div[@class='dropdown-title']/span/a/@title",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 1, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 1, # List Price only Available with JS call
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }       
     


    # Create the Camfere dictionary (source code 67).
    xpath_dict['67'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.camfere.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/kfl47bihe4205609bfdc4298610e15/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=895169&m=67075&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//li[contains(@class, 'productClass')] | //li/div[contains(@class, 'productClass')]",
        "product_list_title":       "h3/a/text()",
        "product_list_url":         "h3/a/@href",
        "next_page":                "//li[contains(@class, 'pageN')]/a/@href",
        "start_urls" : [
            "https://www.camfere.com/new-arrivals/",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":          "https://www.camfere.com/site-map.html",
        "sitemap_link":         "//div[@class='site_map']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":      "//div[contains(@class, 'showInformation')]",
        "title":                "//div[contains(@class, 'showInformation')]/h1/text()",
        "img_url":              "//ul[contains(@class, 'productSmallmove')]/li[1]/a/@href",
        "img_url2":             "//ul[contains(@class, 'productSmallmove')]/li[2]/a/@href",
        "img_url3":             "//ul[contains(@class, 'productSmallmove')]/li[3]/a/@href",
        "list":                 "substring-before(substring-after(//script[contains(text(), 'var product')],  'price\":\"'), '\",')",
        "price":                "substring-before(substring-after(//script[contains(text(), 'var product')],  'saleprice\":\"'), '\",')",
        "stars":                "substring-before(substring-after(//script[@type='application/ld+json'], 'ratingValue\":'), ',\"')",
        "reviews":              "substring-before(substring-after(//script[@type='application/ld+json'], 'reviewCount\":'), '},\"')",
        "sku":                  "//input[@name='productSku']/@value",
        "stock":                "//input[@name='storageId']/@value",
        "description":          "//div[@id='description']/node()",
        "cat":                  "//ul[contains(@class, 'Bread_crumbs')]/li[2]/a/span/text()",
        "sub":                  "//ul[contains(@class, 'Bread_crumbs')]/li[3]/a/span/text()",
        "subsub":               "//ul[contains(@class, 'Bread_crumbs')]/li[4]/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }      
        
    # Create the RCmoment dictionary (source code 68)
    xpath_dict['68'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.rcmoment.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/sr85ll2ww8205609bfdc3f368878d8/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=880750&m=66512&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//li[contains(@class, 'productClass')] | //li/div[contains(@class, 'productClass')]",
        "product_list_title":       "h3/a/text()",
        "product_list_url":         "h3/a/@href",
        "next_page":                "//li[contains(@class, 'pageN')]/a/@href",
        "start_urls" : [
            "https://www.rcmoment.com/new-arrivals/",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":          "https://www.rcmoment.com/site-map.html",
        "sitemap_link":         "//div[@class='site_map']/ul/li/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":      "//div[contains(@class, 'showInformation')]",
        "title":                "substring-before(substring-after(//script[contains(text(), 'var product')],  'title\":\"'), '\",')",
        "img_url":              "//ul[contains(@class, 'productSmallmove')]/li[1]/a/@href",
        "img_url2":             "//ul[contains(@class, 'productSmallmove')]/li[2]/a/@href",
        "img_url3":             "//ul[contains(@class, 'productSmallmove')]/li[3]/a/@href",
        "list":                 "substring-before(substring-after(//script[contains(text(), 'var product')],  'price\":\"'), '\",')",
        "price":                "substring-before(substring-after(//script[contains(text(), 'var product')],  'saleprice\":\"'), '\",')",
        "stars":                "substring-before(substring-after(//script[@type='application/ld+json'], 'ratingValue\":'), ',\"')",
        "reviews":              "substring-before(substring-after(//script[@type='application/ld+json'], 'reviewCount\":'), '},\"')",
        "sku":                  "//input[@name='productSku']/@value",
        "stock":                "//input[@name='storageId']/@value",
        "description":          "//div[@id='description']/node()",
        "cat":                  "//div[contains(@class, 'breadcrumb')]/span/a[1]/text()",
        "sub":                  "//div[contains(@class, 'breadcrumb')]/span/a[2]/text()",
        "subsub":               "//div[contains(@class, 'breadcrumb')]/span/a[3]/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }


    # Create the Romwe dictionary (source code 55)    
    xpath_dict['55'] = {
        # The following items are for the new URL list scraper
        "source_url":               "http://www.romwe.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://www.shareasale.com/r.cfm?u=761764&b=298619&m=32222&afftrack=CIsku&urllink=",
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//div[contains(@class, 'c-goodsli')]",
        "product_list_title":       "a[1]/@title",
        "product_list_url":         "a[1]/@href",
        "next_page":                "//ul[contains(@class, 'page-wrap')]/li[@class='active']/following::li[1]/a/@href",
        "start_urls" : [
            "http://www.romwe.com/daily-new.html?icn=dailynew&ici=rw_navbar01",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":              "http://www.romwe.com/",
        "sitemap_link":             "//div[@class='nav-dropdown']/div[@class='left']/h4/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":          "//div[contains(@class, 'j-goodsd-right')]",
        "title":                    "//h3/text()",
        "img_url":                  "//div[@class='thumbs-wrapper']/div[1]/div/img/@src",
        "img_url2":                 "//div[@class='thumbs-wrapper']/div[2]/div/img/@src",
        "img_url3":                 "//div[@class='thumbs-wrapper']/div[3]/div/img/@src",
        "list":                     "substring-before(substring-after(//script[contains(text(), 'var item1')], 'retailPrice\":{\"amount\":\"'), '\",')",
        "price":                    "substring-before(substring-after(//script[contains(text(), 'var item1')], 'salePrice\":{\"amount\":\"'), '\",')",
        "stars":                    "//dummy",
        "reviews":                  "//dummy",
        "sku":                      "substring-after(//div[@class='sku'], 'SKU:')",
        "stock":                    "substring-before(substring-after(substring-after(//script[contains(text(), 'var item1')], 'is_on_sale'), 'stock\":\"'), '\",')",
        "description":              "//div[contains(@class, 'desc-wrap')][1]/node()",
        "cat":                      "//ul[@class='c-breadcrumb']/li[2]/a/text()",
        "sub":                      "//ul[@class='c-breadcrumb']/li[3]/a/text()",
        "subsub":                   "//ul[@class='c-breadcrumb']/li[4]/a/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars":          1, 
        "empty_reviews":        1,
        "empty_stock":          0,
        "empty_list":           0,
        "empty_cat":            0,
        "empty_sub":            1,
        "empty_subsub":         1,
        "empty_description":    0
        }
    
    
    # Create the Newchic dictionary (source code 69)
    xpath_dict['69'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.newchic.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/0i4jszvwip205609bfdc3442850f04/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=820550&m=63433&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//li[contains(@class, 'wom_lst_detail')]",
        "product_list_title":       "div[contains(@class, 'use_wom_lst')]/div[@class='wom_lst_btm']/h1/a/@title",
        "product_list_url":         "div[contains(@class, 'use_wom_lst')]/div[@class='wom_lst_btm']/h1/a/@href",
        "next_page":                "//div[contains(@class, 'page_num')]/a[position()=last()]/@href",
        "start_urls" : [
            "https://www.newchic.com/new-arrivals/",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":              "https://www.newchic.com/",
        "sitemap_link":             "//span[@class='menu']/a/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":          "//div[@id='maindet']",
        "title":                    "//meta[@property='og:title']/@content",
        "img_url":                  "//ul[@class='img-list']/li[1]/div/img/@data-big-img",
        "img_url2":                 "//ul[@class='img-list']/li[2]/div/img/@data-big-img",
        "img_url3":                 "//ul[@class='img-list']/li[3]/div/img/@data-big-img",
        "list":                     "//span[@class='price_old']/@oriprice",
        "price":                    "//div[@class='price_number']/@oriprice",
        "stars":                    "//ul[contains(@class, 'star-container')]/li/span[contains(@class, 'score')]",
        "reviews":                  "//ul[contains(@class, 'star-container')]/li/span[contains(@class, 'reviews_count')]",
        "sku":                      "//li[@id='showSku']/span/text()",
        "stock":                    "//meta[@itemprop='availability']/@content",
        "description":              "//div[@class='detail_content description']/div[1][not(text()= '{ \"id\" : \"Specification\", \"title\" : [], \"data\" : []}')] | //div[@class='detail_content description']/span",
        "cat":                      "//ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][2]/a/span/text() | //ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][2]/b/a/span/text()",
        "sub":                      "//ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][3]/a/span/text() | //ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][3]/b/a/span/text()",
        "subsub":                   "//ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][4]/a/span/text() | //ul[contains(@itemtype, 'Breadcrumb')]/li[@itemprop='itemListElement'][4]/b/a/span/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 1,
        "empty_description": 0
        }

        
    """
    # Create the YesStyle dictionary (source code 70)
    xpath_dict['70'] = {
        # The following items are for the new URL list scraper
        "source_url": "http://www.yesstyle.com",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "https://www.shareasale.com/r.cfm?u=761764&b=61830&m=10669&afftrack=CIsku&urllink=",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "//div[@class='itemContainer']",
        "product_list_title": "a/div[@class='itemTitle']/text()",
        "product_list_url": "a/@href",
        "next_page": "//a[@aria-label='Next Page']/@href",
        "start_urls" : [
            "http://www.yesstyle.com/en/women-beauty/list.html/bcc.14072_bpt.46?oc=1&sb=158",
            "http://www.yesstyle.com/en/women-clothing/list.html/bcc.14071_bpt.46?oc=1&sb=158",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "",
        "sitemap_link": "",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "//div[contains(@class, 'productInfo')]",
        "title": "normalize-space(concat(//h1/span[contains(@ng-show, 'brandName')]/span, ' ', //h1/span[contains(@ng-bind-html, 'product.name')]))",
        "img_url": "",
        "img_url2": "",
        "img_url3": "",
        "list": "",
        "price": "",
        "stars": "",
        "reviews": "",
        "sku": "",
        "stock": "",
        "description": "",
        "cat": "",
        "sub": "",
        "subsub": "",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 0,
        "empty_description": 0
        }
    """
       

    # Create the Rotita dictionary (source code 71)
    xpath_dict['71'] = {
        # The following items are for the new URL list scraper
        "source_url":               "https://www.rotita.com/",
        "query_url":                "",
        "na_url":                   "",
        "affiliate_link_before":    "https://ad.admitad.com/g/wo18bv3kmr205609bfdc9144236bbd/?subid=CIsku&ulp=", # https://www.shareasale.com/r.cfm?u=761764&b=494342&m=48174&afftrack=CIsku&urllink=
        "affiliate_link_after":     "",
        # (new arrivals).
        "product_list_item":        "//div[contains(@class, 'box-product-list_THR')]/div[@class='wen150'] | //li[@class='cat_item']/div[@class='proImg']",
        "product_list_title":       "a/@title",
        "product_list_url":         "a/@href",
        "next_page":                "//div[contains(@class, 'pageList')]/p/a[contains(text(), 'Next')]/@href",
        "start_urls" : [
            "https://www.rotita.com/whats_new.html",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url":              "https://www.rotita.com",
        "sitemap_link":             "//td[@class='cat_box']/dl/dt/a[contains(text(), 'View all' )]/@href",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper":          "//div[contains(@class, 'pro_content')]",
        "title":                    "//h1/text()",
        "img_url":                  "//ul[@class='js_scrollableDiv']/li[1]/img/@data-big-img",
        "img_url2":                 "//ul[@class='js_scrollableDiv']/li[2]/img/@data-big-img",
        "img_url3":                 "//ul[@class='js_scrollableDiv']/li[3]/img/@data-big-img",
        "list":                     "//span[@id='unit_price']/@orgp",
        "price":                    "//div[@id='MY_PRICE']/@orgp",
        "stars":                    "//dummy", #They get this values with XHR call to dynamic.php
        "reviews":                  "//dummy", #They get this values with XHR call to dynamic.php
        "sku":                      "substring-before(substring-after(//script[@type='text/javascript' and contains(text(), 'goods_id')],  'goods_id=\"'), '\";')",
        "stock":                    "//meta[@itemprop='availability']/@content",
        "description":              "//div[@class='goods-detail']/dl[@class='mt10']/node()",
        "cat":                      "//div[@id='ur_here']/a[2]/text()",
        "sub":                      "//div[@id='ur_here']/a[3]/text()",
        "subsub":                   "//div[@id='ur_here']/a[4]/text()",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars":              1, 
        "empty_reviews":            1,
        "empty_stock":              1,
        "empty_list":               0,
        "empty_cat":                0,
        "empty_sub":                1,
        "empty_subsub":             1,
        "empty_description":        0
        }
        
        
    # Template dictionary 
    """
    xpath_dict[''] = {
        # The following items are for the new URL list scraper
        "source_url": "",
        "query_url": "",
        "na_url": "",
        "affiliate_link_before": "",
        "affiliate_link_after": "",
        # (new arrivals).
        "product_list_item": "",
        "product_list_title": "",
        "product_list_url": "",
        "next_page": "",
        "start_urls" : [
            "",
            ],
        # The next items are for the Sitemap Products Scraper
        "sitemap_url": "",
        "sitemap_link": "",
        # The next list of items are for a specific product URL scrape.
        "product_wrapper": "",
        "title": "",
        "img_url": "",
        "img_url2": "",
        "img_url3": "",
        "list": "",
        "price": "",
        "stars": "",
        "reviews": "",
        "sku": "",
        "stock": "",
        "description": "",
        "cat": "",
        "sub": "",
        "subsub": "",
        # The next items are to overrule the empty error value by setting to 1
        "empty_stars": 0, 
        "empty_reviews": 0,
        "empty_stock": 0,
        "empty_list": 0,
        "empty_cat": 0,
        "empty_sub": 0,
        "empty_subsub": 0,
        "empty_description": 0
        }
    """
        
    # Return the dictionary
    return xpath_dict