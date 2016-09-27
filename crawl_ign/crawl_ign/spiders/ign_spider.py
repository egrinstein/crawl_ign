# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from ..items import IGNItem

class IGNItem(scrapy.Item):
    title = scrapy.Field()
    genre = scrapy.Field()
    platform = scrapy.Field()
    release_date = scrapy.Field()
    score = scrapy.Field()
    score_phrase = scrapy.Field()
    editors_choice = scrapy.Field()
    url = scrapy.Field()

BASE_AJAX_REQUEST = "http://www.ign.com/games/reviews-ajax?startIndex="
N_GAMES = 18601 # empirical data :)

def save_body(bd,fn):
    with open(fn,'wt') as f:
        f.write(bd)

class IgnSpider(scrapy.Spider):
    name = "ign_spider"
    allowed_domains = ["http://www.ign.com","ign.com"]
    start_urls = (
            "http://www.ign.com/games/reviews",
    ) # the first request is just for getting them sweet cookiez

    def parse(self, response):
        
        i=0
        n_loops = N_GAMES/25 + 1 # API yields 25 titles at a time
        for i in range(n_loops):  
            next_request = BASE_AJAX_REQUEST+str(25*i)
            yield Request(next_request,
                          callback=self.parse_details)
    def parse_details(self,response):
        item_nodes = Selector(text=response.body).xpath('//div[@class="clear itemList-item"]')
        if len(item_nodes) != 25:
            print len(item_nodes)
        for node in item_nodes:
            item = IGNItem()
            title_node = node.xpath('.//div[@class="item-title"]')
            title = title_node.xpath('h3/a/text()').extract_first()
            item['url'] = title_node.xpath('h3/a/@href').extract_first()
            item['title'] = title.strip()
            item['platform'] = title_node.xpath('h3/span/text()').extract_first()
            
            details_node = node.xpath('.//p[@class="item-details"]')
            item['genre'] = details_node.xpath('span/text()').extract_first().strip()
            
            
            item['release_date'] = node.xpath('.//div[@class="grid_3"]/div/text()').extract_first()
            
            review_node = node.xpath('.//div[@class="releaseDate grid_3 omega"]')
            editors_choice = review_node.xpath('div[@class="editorsChoice"]/text()')
            if editors_choice:
                item['editors_choice'] = 'Y'
            else:
                item['editors_choice'] = 'N'
            item['score'] = review_node.xpath('.//span[@class="scoreBox-score"]/text()').extract_first()
            item['score_phrase'] = review_node.xpath('.//span[@class="scoreBox-scorePhrase"]/text()').extract_first()
            

            yield item
