import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import AlrajhibanksaItem
from itemloaders.processors import TakeFirst


class AlrajhibanksaSpider(scrapy.Spider):
	name = 'alrajhibanksa'
	start_urls = ['https://www.alrajhibank.com.sa/ar/sxa/search/results/?s={30785871-3921-4466-BE3B-6A762E458781}&itemid={A692D3DA-2803-4D5D-8499-CEA83616C09F}&sig=pressreleases&p=999999&e=0']

	def parse(self, response):
		post_links = [i['Url'] for i in json.loads(response.text)['Results']]
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h3[@class="pws-title-article field-title"]/text()').get()
		description = response.xpath('//div[@class="pws-article-content field-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="pws-article-date field-publisheddate"]/text()').get()

		item = ItemLoader(item=AlrajhibanksaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
