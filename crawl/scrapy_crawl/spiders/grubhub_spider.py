import json
from typing import Iterator

import scrapy

import project_settings as s
from crawl.starter import start_scrapy_crawl

BRAND = "GRUBHUB"
CLIENT_ID = "beta_UmWlpstzQSFmocLy3h1UieYcVST"
DEVICE_ID = 1844483276
SCOPE = "anonymous"


class GrubhubSpiderSpider(scrapy.Spider):
    name = "grubhub_spider"
    allowed_domains = ["www.grubhub.com", "grubhub.com"]
    custom_settings = {"SMARTPROXY_COUNTRY": "us"}

    def start_requests(self) -> Iterator[scrapy.Request]:
        yield scrapy.Request(
            url="https://api-gtm.grubhub.com/auth",
            method="POST",
            # callback=self.parse,
            # errback=self.handle_errback,
            headers={
                "Content-Type": "application/json;charset=UTF-8",
                "Authorization": "Bearer",
            },
            # cb_kwargs=dict(params=params),
            body=json.dumps(
                {
                    "brand": BRAND,
                    "client_id": CLIENT_ID,
                    "device_id": DEVICE_ID,
                    "scope": SCOPE,
                }
            ),
            # dont_filter=True,
        )

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":
    spider_names = ["grubhub_spider"]

    start_scrapy_crawl(
        spider_names=spider_names,
        max_requests=1,
        output_folder=s.OUTPUT_FOLDER,
    )
