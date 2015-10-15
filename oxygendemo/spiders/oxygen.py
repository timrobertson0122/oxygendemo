# -*- coding: utf-8 -*-
import scrapy
from oxygendemo.items import OxygendemoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery

class OxygenSpider(CrawlSpider):
    name = "oxygenboutique.com"
    allowed_domains = ["oxygenboutique.com"]
    start_urls = ['http://www.oxygenboutique.com/clothing.aspx',
                  'http://www.oxygenboutique.com/Shoes-All.aspx',
                  'http://www.oxygenboutique.com/accessories-all.aspx',
                  'http://www.oxygenboutique.com/Sale-In.aspx'
    ]
#   # to find appropriate category listing pages,
#   # to identify individual product pages (this rule should have a callback='parse_item'),
    rules = (
        Rule(LinkExtractor(allow=('boots.aspx', ), deny=('designers.aspx', ))),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('Running-sneaker.aspx', )), callback='parse_item'),
    )

    def parse_item(self, response):
        pq = PyQuery(response.body)
        item = OxygendemoItem()
        item['designer'] = self.item_designer(pq)
        item['name'] = self.item_name(pq)
        item['link'] = response.url
        
        return item

    def item_designer(self, pq):
        return pq('.brand_name a').text()
    
    def item_name(self, pq):
        return pq('h2').text()