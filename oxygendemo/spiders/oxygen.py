# -*- coding: utf-8 -*-
from oxygendemo.items import OxygendemoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery


class OxygenSpider(CrawlSpider):
    name = "oxygenboutique.com"
    allowed_domains = ["oxygenboutique.com"]
    start_urls = [
        'http://www.oxygenboutique.com/clothing.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/Shoes-All.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/accessories-all.aspx?ViewAll=1',
        'http://www.oxygenboutique.com/Sale-In.aspx?S=1&ViewAll=1'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.DataContainer')),
             callback='parse_item'),
    )

    def item_code(self, response):
        return response.url.split('/')[-1].split('.')[0].lower()

    def item_designer(self, el):
        return el('.brand_name a').text()

    def item_name(self, el):
        return el('h2').text()

    def item_url(self, response):
        return response.url

    def item_gbp_price(self, el):
        if el('.offsetMark').text() != (''):
            price = el('.offsetMark').text()
        else:
            price = el('.price').text()
        return price

    def item_sale_discount(self, el):
        if el('.offsetMark').text() != (''):
            original_price_int = eval(el('.offsetMark').text())
            sale_price_int = eval(el('.price').text().split(' ')[-1])
            discount_percent = (sale_price_int / original_price_int) * 100
            return discount_percent

    def item_description(self, el):
        return el('h3').eq(0).next().text()

    def item_images(self, el):
        img_array = []
        for i in el('img[src*="GetImage"]'):
            img_array.append(i.attrib["src"])
        return img_array

    def item_stock_status(self, el):
        stock_dict = {}
        for i in el('.productpage_box option'):
            if "Please Select" not in i.text:
                if "Sold Out" not in i.text:
                    stock_dict.update({i.text: 3})
                else:
                    d = i.text.split(' ')[0]
                    stock_dict.update({d: 1})
        return stock_dict

    def item_raw_color(self, el):
        return 'None'

    def item_gender(self, el):
        return 'F'

    def is_item_jewellery(self, el):
        product_description = el('h3').eq(0).next().text().lower()
        jewellery_list = ['bangle', 'bangles', 'bracelet', 'choker', 'ear',
                          'earring', 'earrings', 'necklace', 'ring']
        if any(word in product_description.split() for word in jewellery_list):
            return True

    def item_type(self, el, response):
        referer_category = response.request.headers.get('Referer', None)
        if "clothing" in referer_category:
            return 'A'
        elif "Shoes" in referer_category:
            return 'S'
        elif "accessories" in referer_category:
            if self.is_item_jewellery(el) is True:
                return 'J'
            else:
                return 'R'
        else:
            return 'Unknown - Sale Item'

    def parse_item(self, response):
        el = PyQuery(response.body)
        item = OxygendemoItem()
        item['code'] = self.item_code(response)
        item['designer'] = self.item_designer(el)
        item['name'] = self.item_name(el)
        item['link'] = self.item_url(response)
        item['gbp_price'] = self.item_gbp_price(el)
        item['raw_color'] = self.item_raw_color(el)
        item['gender'] = self.item_gender(el)
        item['description'] = self.item_description(el)
        item['sale_discount'] = self.item_sale_discount(el)
        item['images'] = self.item_images(el)
        item['stock_status'] = self.item_stock_status(el)
        item['type'] = self.item_type(el, response)
        yield item
