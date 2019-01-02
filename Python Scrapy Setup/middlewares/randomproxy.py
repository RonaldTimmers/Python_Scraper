# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
import logging
import ProxyService

class RandomProxyMiddleware(object):
    def __init__(self, settings):
        super(RandomProxyMiddleware, self).__init__()
        # Get proxies from Linode 'proxies' table
        # ProxyService is added service in site-packages
        try:
            proxy_list = ProxyService.get_proxies()
        except:
            logging.critical('Failed to get proxies')
            
        # logging.info('proxy_list: %s', proxy_list)
        
        self.proxies = []
        # user_pass = 'eekhoorn:hamsteren'
        
        for proxy in proxy_list:
            # Loop through the query result and write down in proxies
            self.proxies.append('http://' + str(proxy[0]) + ':' + str(proxy[1]))
        
        
        '''
        #fin = open(self.proxy_list)
        for line in fin.readlines():
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line)

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''
            
            print user_pass
            print parts.group(1)
            print parts.group(3)
            
            self.proxies[parts.group(1) + parts.group(3)] = user_pass

        fin.close()
        '''
        
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return
            
        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')
        
        try:
            # logging.info('self.proxies: %s', self.proxies)
            self.proxy_address = random.choice(self.proxies)
            request.meta['proxy'] = self.proxy_address
            # logging.info('Request.meta["proxy"] %s', request.meta['proxy'])
            return
        except:
            logging.critical("No Random Proxy Selected!")
        """
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass) # Changed from: base64.encodestring(proxy_user_pass), After some proxy bugs
            request.headers['Proxy-Authorization'] = basic_auth
        """
        
        
    def process_response(self, request, response, spider):
        # logging.debug('Response.meta["proxy"]: {}'.format(request.meta['proxy']))
        return response

    def process_exception(self, request, exception, spider):
        
        #log.msg('Removing failed proxy <%s>, %d proxies left' % (
        #            proxy, len(self.proxies)))
        
        # logging.info('Removing failed proxy <%s>', request.meta['proxy'])
        try:
            # del self.proxies[request.meta['proxy']]
            logging.info('request: %s', request)
        except ValueError:
            pass