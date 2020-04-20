import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import re
import json


lua_script = """
function main(splash)
    local num_scrolls = 100
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        admicroAD.unit.push(function () { admicroAD.show('admzone14092') });
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
end
"""


class CrawlerNews(scrapy.Spider):

	name = "stock"

	def start_requests(self):
		urls = [
				"https://s.cafef.vn/screener.aspx#data"
		]
		for url in urls:
			# yield SplashRequest(url=url, endpoint = "render.html", callback=self.parse)
			yield SplashRequest(url=url, callback=self.parse,
                                endpoint="execute",
                                args={'wait': 2, 'lua_source': lua_script},)

	def parse(self, response):
		"""
		"""
		print(">>res: ", response.css("#myTable").css("tbody"))
		for item in response.css("#data").css("tbody"):
			row = item.css(".symbol").css("a::text").extract_first()
			print(row)
			
				
			yield item
