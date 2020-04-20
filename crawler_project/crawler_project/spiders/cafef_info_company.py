import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import re
from scrapy.http import Request
import os
import tqdm
import logging
import requests
import json

paths = ['data/pdf', 'logs']
for path in paths:
	print("Checking make sure that path exists !")
	if not os.path.exists(path):
		os.makedirs(path)


def get_file(url):
	"""
		params: Link to file pdf
		return: write file pdf if exists
	"""
	try:
		file = requests.get(url, allow_redirects=True)
		name = url.split("/")[-1]
		path = os.path.join("data/pdf", name)
		open(path, 'wb').write(file.content)
	except Exception as e:
		with open('logs/log_dowload_pdf.txt', 'a') as f:
			f.write(str(e))
		pass


class CrawlerInfo(scrapy.Spider):

	name = "info"

	def start_requests(self):
		urls = [
				# "https://s.cafef.vn/Tin-doanh-nghiep/fpt/Event.chn"
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=FPT&floorID=0&configID=0&PageIndex=1&PageSize=10000&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=FPT&floorID=0&configID=0&PageIndex=1&PageSize=30&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=HPS&floorID=0&configID=0&PageIndex=1&PageSize=200&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=CRE&floorID=0&configID=0&PageIndex=1&PageSize=150&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=A32&floorID=0&configID=0&PageIndex=1&PageSize=100&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=AAA&floorID=0&configID=0&PageIndex=1&PageSize=1000&Type=2",
				"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=ABI&floorID=0&configID=0&PageIndex=1&PageSize=1000&Type=2"


		]

		for url in urls:
			print(">>: ", url)
			print("ress", scrapy.Request(url=url, method='GET').body)
			yield scrapy.Request(url=url, method='GET', callback=self.parse)
			# yield SplashRequest(url=url, callback=self.parse,
								# endpoint="execute",
								# args={'wait': 2, 'lua_source': lua_script},)
	def parse_detail(self, response):
		"""
			Get response in detail all item in parse func
		"""
		item = response.request.meta['item']
		body = response.css(".mainDetailV2")
		content = body.css("#newscontent")
		file = content.css("div a::attr(href)").extract_first()
		try:
			if file.endswith(".pdf"):
				item["link_pdf"] = file
				tqdm.tqdm(get_file(file))
			else:
				item["link_info"] = file
		except Exception as e:
			with open('logs/logs_pdf.txt', 'a') as f:
				f.write(str(e))
			pass

		yield item


	def parse(self, response):
		"""
			Get response all item in pages
		"""
		all_data = []
		link_duplicated = []
		for item in tqdm.tqdm(response.css("#divEvents").css("ul").css('li')):
			link = item.css("a::attr(href)").extract_first()
			if link not in link_duplicated:
				link_duplicated.append(link)
				item_crawler = {
						"title": item.css('li a::attr(title)').extract_first(),
						"link": "s.cafef.vn"+link

				}		
				print(item_crawler)
				yield response.follow(link, callback=self.parse_detail, meta={'item': item_crawler})
		# yield SplashRequest(
  #           url=response.url,
  #           callback=self.parse,
  #           meta={
  #               "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
  #           },
  #       )

	def parse_product_page(self, response):
		"""
		The crawler page use scrapy to get the data, try to analyze it and finish it
		by yourself.
		"""
		logging.info("processing " + response.url)
		yield None