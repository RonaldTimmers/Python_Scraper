from fake_useragent import UserAgent
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import logging
import random

class RandomUserAgentMiddleware(UserAgentMiddleware):
    
    def __init__(self, settings):
        super(RandomUserAgentMiddleware, self).__init__()
        
        
        user_agent_list_file = settings.get('USER_AGENT_LIST')
        
        if not user_agent_list_file:
            self.ua = UserAgent(cache=False)
            # self.ua.update()
        else:
            with open(user_agent_list_file, 'r') as f:
                self.user_agent_list = [line.strip() for line in f.readlines()]
    
    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj


    
    def process_request(self, request, spider):
        if self.user_agent_list:
            random_useragent = random.choice(self.user_agent_list)
            logging.debug('Useragent List: {}'.format(random_useragent))
        else:
            random_useragent = self.ua.random
            logging.debug('Useragent Fake: {}'.format(random_useragent))
        
        request.headers.setdefault('User-Agent', random_useragent)
        
        
    """
    def process_response(self, request, response, spider):
        logging.debug('Useragent: {}'.format(request.headers.get('User-Agent')))
        
        return response
    """