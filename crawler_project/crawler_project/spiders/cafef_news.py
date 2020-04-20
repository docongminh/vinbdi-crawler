import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import re
import json


# lua_script = """
# function main(splash)
#     local num_scrolls = 100
#     local scroll_delay = 1.0
#     local scroll_to = splash:jsfunc("window.scrollTo")
#     local get_body_height = splash:jsfunc(
#         "function() {return document.body.scrollHeight;}"
#     )
#     assert(splash:go(splash.args.url))
#     splash:wait(splash.args.wait)
#     for _ = 1, num_scrolls do
#         scroll_to(0, get_body_height())
#         splash:wait(scroll_delay)
#     end
#     return splash:html()
# end
#"""
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

	name = "news"

	def start_requests(self):
		urls = [
				"https://cafef.vn/thoi-su.chn"
		]

		# script = """
		# 	function main(splash)
		# 	local url = splash.args.url
		# 	assert(splash:go(url))
		# 	assert(splash:wait(0.5))
		# 	assert(splash:runjs("$('.next')[0].click();"))
		# 	return {
		# 	html = splash:html(),
		# 	url = splash:url(),
		# 	}
		# 	end
		# """

		for url in urls:
			# yield SplashRequest(url=url, endpoint = "render.html", callback=self.parse)
			yield SplashRequest(url=url, callback=self.parse,
                                endpoint="execute",
                                args={'wait': 2, 'lua_source': lua_script},)

	def parse(self, response):
		"""
		"""
		all_data = []
		link_duplicated = []
		for item in response.css(".tlitem"):
			link = item.css("h3 a::attr(href)").extract_first()
			if link not in link_duplicated:
				link_duplicated.append(link)
				item_crawler = {
						"title": item.css('h3 a::attr(title)').extract_first(),
						"link": link,
						"image": item.css('a img::attr(src)').extract_first(),
						"time": item.css(".knswli-right").css("p span::attr(title)").extract_first(),
						"sub_content": item.css(".knswli-right").css(".sapo::text").extract_first()

				}
				print("tesst: ", item_crawler)
				
				# with open('result.json', 'a', encoding='utf-8') as fp:
				# 	json.dump(item_crawler, fp, indent=1)
			yield item
		# 		yield response.follow(link, meta={'item': item_crawler})
		# view_more = response.css(".bt_xemthem").css("a::attr(href)").extract_first()
		# if view_more is not None:
		# 	yield response.follow(view_more, callback=self.parse)

