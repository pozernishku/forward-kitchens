import scrapy

import project_settings as s
from crawl.starter import start_scrapy_crawl


class GrubhubSpiderSpider(scrapy.Spider):
    name = "grubhub_spider"
    allowed_domains = ["www.grubhub.com", "grubhub.com"]
    custom_settings = {"SMARTPROXY_COUNTRY": "us"}

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":
    spider_names = ["grubhub_spider"]

    start_scrapy_crawl(
        spider_names=spider_names,
        max_requests=1,
        output_folder=s.OUTPUT_FOLDER,
    )
