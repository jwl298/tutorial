# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#class TutorialPipeline(object):
    #def process_item(self, item, spider):
        #return item

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log
from scrapy import signals


'''class DuplicatesPipeline(object):

    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.titles_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.titles_seen.add(item['title'])
            return item'''

class NoData(object):
    def process_item(self, item, spider):
        if len(item['title']) > 0:
            return item
        else:
            raise DropItem("Missing title in %s" % item)

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        
    def process_item(self, item, spider):
    	valid = True
        for data in item:
          # here we only check if the data is not null
          # but we could do any crazy validation we want
       	  if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
          self.collection.insert(dict(item))
          log.msg("Item wrote to MongoDB database %s/%s" %
                  (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                  level=log.DEBUG, spider=spider) 
        return item