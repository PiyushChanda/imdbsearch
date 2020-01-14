# -*- coding: utf-8 -*-
from scrapy import Spider, Request, Item, Field

class MoviesSpider(Spider):
	name = 'movies'
	allowed_domains = ['imdb.com']
	start_urls = ['https://www.imdb.com/title/tt7286456']

	def parse(self, response):
		name = response.xpath('//h1/text()').extract_first()
		year = response.xpath('//span[@id="titleYear"]/a/text()').extract_first()
		url_of_movies = response.xpath('//div[contains(@class,"rec_page")]//a/@href').extract()
		full_url_of_movies = [response.urljoin(url) for url in url_of_movies]
		imdb_rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
		metacritic_score = response.xpath('//a[@href="criticreviews"]//span/text()').extract_first()

		yield {
				'name': name,
				'year': year,
				'imdb_rating': imdb_rating,
				'metacritic_score': metacritic_score,
				'url': response.url
			}

		for url in full_url_of_movies:
			yield Request(url, callback=self.parse_movie)

	def parse_movie(self, response):
		name = response.xpath('//h1/text()').extract_first()
		year = response.xpath('//span[@id="titleYear"]/a/text()').extract_first()
		imdb_rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
		metacritic_score = response.xpath('//a[@href="criticreviews"]//span/text()').extract_first()

		yield {
				'name': name,
				'year': year,
				'imdb_rating': imdb_rating,
				'metacritic_score': metacritic_score,
				'url': response.url
			}

# Run Scrapy RT
# http://localhost:9080/crawl.json?spider_name=movies&url=https://www.imdb.com/title/tt3065204/
