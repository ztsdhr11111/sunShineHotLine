# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SunshineHotlineItem


class SuncSpider(CrawlSpider):
    name = 'sunc'
    allowed_domains = ['wz.sun0769.com']

    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']


    rules = (
        Rule(LinkExtractor(allow='type=4'), process_links='deal_links', follow=True),
        Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parse_item')
    )

    def deal_links(self, links):
        for link in links:
            link.url = link.url.replace('?', '&').replace('Type&', 'Type?')
            print(link.url)
        return links

    def parse_item(self, response):
        print(response.url)
        item = SunshineHotlineItem()
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3"]//strong/text()').extract()
        item['number'] = item['title'].split(' ')[-1].split(':')[-1]
        content = response.xpath('//div[@class="contextext"]/text()').extract()
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            item['content'] = ''.join(content).strip()
        else:
            item['content'] = ''.join(content).strip()

        item['url'] = response.url

        yield item
