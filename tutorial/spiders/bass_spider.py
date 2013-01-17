from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BassItem

import logging
from scrapy.log import ScrapyFileLogObserver

logfile = open('testlog.log', 'w')
log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
log_observer.start()


class BassSpider(CrawlSpider):
    name = "bass"
    allowed_domains = ["talkbass.com"]
    start_urls = ["http://www.talkbass.com/forum/f126"]


    rules = [Rule(SgmlLinkExtractor(allow=['/f126/index*']), callback='parse_item', follow=True, restrict_xpaths=('//a[@title = 'Next Page']')]


    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)


        ads = hxs.select('//table[@id="threadslist"]/tbody/tr/td[@class="alt1"][2]/div')
        items = []
        for ad in ads:
            item = BassItem()
            item['title'] = ad.select('a/text()').extract()
            item['link'] = ad.select('a/@href').extract()
            items.append(item)
        return items

