# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BassItem(Item):
	title = Field()
	link = Field()
	print title, link
