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
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(restrict_css=('li.tame', ), deny=('/[0-9]{2,}/', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(restrict_css=('li.tame', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = OxygendemoItem()
        item['link'] = response.url
        item['code'] = response.css('h2::text').extract()
        item['usd_price'] = response.css('span.price').extract()
        item['description'] = response.css('div#ui-accordion-accordion-panel-0.innerHtml').extract()
        return item