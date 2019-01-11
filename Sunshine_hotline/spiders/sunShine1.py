# -*- coding: utf-8 -*-
import scrapy
from ..items import SunshineHotlineItem

class Sunshine1Spider(scrapy.Spider):
    name = 'sunShine1'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0

    start_urls = [url + str(offset)]

    def parse(self, response):
        links = response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract()

        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

        if self.offset <= 71130:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        print(response.url)
        item = SunshineHotlineItem()
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract_first()
        item['number'] = item['title'].split(' ')[-1].split[':'][-1]
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            item['content'] = ''.join(content).strip()
        else:
            item['content'] = ''.join(content).strip()

        item['url'] = response.url

        yield item