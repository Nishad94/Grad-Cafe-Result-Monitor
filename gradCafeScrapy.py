import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GradcafeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    school = scrapy.Field()
    branch = scrapy.Field()
    degree = scrapy.Field()
    stats = scrapy.Field()
    via = scrapy.Field()
    #comments = scrapy.Field()
    decision = scrapy.Field()
    pass

class GcSpider(scrapy.Spider):
	name = "GradCafe"
	allowed_domains = ["thegradcafe.com"]
	start_urls = [
		"http://www.thegradcafe.com/survey/index.php?t=n&o=&pp=250",
	]

	def parse(self, response):
		for sel in response.xpath('//tr[@onmouseout="hideControlsBox(this);"]'):
			via = sel.xpath('td[3]/text()').extract()[0]
			if via.find('E-mail') != -1 or via.find('Phone') != -1 or via.find('Website') != -1:
				item = GradcafeItem()
				item['school'] = sel.xpath('td[1]/text()').extract()[0]
				branch_deg = sel.xpath('td[2]/text()').extract()[0].split(',')
				if len(branch_deg) == 2:
					item['branch'] = branch_deg[0]
					item['degree'] = branch_deg[1] 
				item['via'] = via
				if sel.xpath('td/a').extract():
					item['stats'] = sel.xpath('td/a').extract()[0]
				#item['comments'] = sel.xpath('td/ul/li[@class="controlspam"]/text()').extract()[0]
				if sel.xpath('td/span[contains(@class, "d")]').extract():
					item['decision'] = sel.xpath('td/span[contains(@class, "d")]/text()').extract()[0]
				yield item


def run_proc_scrapy(file_name):
	settings = get_project_settings()
	settings.set('FEED_FORMAT','json')
	settings.set('FEED_URI', file_name)

	process = CrawlerProcess(settings)

	process.crawl(GcSpider)
	process.start() # the script will block here until the crawling is finished
	print 'exiting\n\n'