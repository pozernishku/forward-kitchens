import scrapy


class GrubhubSpiderSpider(scrapy.Spider):
    name = "grubhub_spider"
    allowed_domains = ["www.grubhub.com", "grubhub.com"]

    def parse(self, response):
        pass
