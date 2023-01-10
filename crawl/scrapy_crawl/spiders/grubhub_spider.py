import scrapy


class GrubhubSpiderSpider(scrapy.Spider):
    name = "grubhub_spider"
    allowed_domains = ["www.grubhub.com", "grubhub.com"]
    custom_settings = {"SMARTPROXY_COUNTRY": "us"}

    def parse(self, response, **kwargs):
        pass
