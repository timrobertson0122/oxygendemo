# -*- coding: utf-8 -*-
import scrapy
from oxygendemo.items import OxygendemoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery

class OxygenSpider(CrawlSpider):
    name = "oxygenboutique.com"
    allowed_domains = ["oxygenboutique.com"]
    start_urls = ['http://www.oxygenboutique.com/clothing.aspx?ViewAll=1', 'http://www.oxygenboutique.com/Shoes-All.aspx?ViewAll=1', 'http://www.oxygenboutique.com/accessories-all.aspx?ViewAll=1', 'http://www.oxygenboutique.com/Sale-In.aspx?S=1&ViewAll=1']

    rules = (
        Rule(LinkExtractor(restrict_css=('.DataContainer')), callback='parse_item'),
    )

    def item_code(self, response):
        return response.url.split('/')[-1].split('.')[0].lower()

    def item_designer(self, pq):
        return pq('.brand_name a').text()
    
    def item_name(self, pq):
        return pq('h2').text()

    def item_url(self, response):
        return response.url

    def item_gbp_price(self, pq):
        if pq('.offsetMark').text() != (''):
          price = pq('.offsetMark').text()
        else:
          price = pq('.price').text()
        return price

    def item_sale_discount(self, pq):
        if pq('.offsetMark').text() != (''):
          original_price_int = eval(pq('.offsetMark').text())
          sale_price_int = eval(pq('.price').text().split(' ')[-1])
          discount_percent = (sale_price_int / original_price_int) * 100
          return discount_percent

    def item_description(self, pq):
        return pq('h3').eq(0).next().text()

    def item_images(self, pq):
        img_array = []
        for i in pq('img[src*="GetImage"]'):
          img_array.append(i.attrib["src"])
        return img_array
     
    def item_stock_status(self, pq):
        stock_dict = {}
        for i in pq('.productpage_box option'):
          if not "Please Select" in i.text: 
            if not "Sold Out" in i.text:
              stock_dict.update({i.text:3})
            else:
              d = i.text.split(' ')[0]
              stock_dict.update({d:1})
        return stock_dict  

    def item_raw_color(self, pq):
      return 'None'

    def item_gender(self, pq):
      return 'F'

    def item_type(self, response):
      referer = response.request.headers.get('Referer', None)
      if "clothing" in referer:
        return 'A'
      elif "Shoes" in referer:
        return 'S'
      elif "accessories" in referer:
        return 'R'
      else:
        return 'Unknown'

    def parse_item(self, response):
        pq = PyQuery(response.body)
        item = OxygendemoItem()
        item['code'] = self.item_code(response)
        item['designer'] = self.item_designer(pq)
        item['name'] = self.item_name(pq)
        item['link'] = self.item_url(response)
        item['gbp_price'] = self.item_gbp_price(pq)
        item['raw_color'] = self.item_raw_color(pq)
        item['gender'] = self.item_gender(pq)
        item['description'] = self.item_description(pq)
        item['sale_discount'] = self.item_sale_discount(pq)
        item['images'] = self.item_images(pq)
        item['stock_status'] = self.item_stock_status(pq)
        item['type'] = self.item_type(response)
        yield item

    