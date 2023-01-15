import json
from typing import Iterator

from scrapy import Spider
from scrapy.http import Request, Response
from scrapy.utils.project import get_project_settings

import project_settings as s
from crawl.starter import start_scrapy_crawl

BRAND = "GRUBHUB"
CLIENT_ID = "beta_UmWlpstzQSFmocLy3h1UieYcVST"
DEVICE_ID = 1844483276
SCOPE = "anonymous"


class GrubhubSpiderSpider(Spider):
    name = "grubhub_spider"
    allowed_domains = ["www.grubhub.com", "grubhub.com"]

    settings = get_project_settings()
    download_handlers = dict(settings.get("DOWNLOAD_HANDLERS"))
    download_handlers.update(
        {
            "http": "scrapy_crawl.handlers.RotatingProxiesDownloadHandler",
            "https": "scrapy_crawl.handlers.RotatingProxiesDownloadHandler",
        }
    )
    custom_settings = {
        "SMARTPROXY_COUNTRY": "us",
        "DOWNLOAD_HANDLERS": download_handlers,
    }

    def start_requests(self) -> Iterator[Request]:
        yield Request(
            url="https://api-gtm.grubhub.com/auth",
            method="POST",
            callback=self.parse_access_token,
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

    def parse_access_token(self, response: Response) -> Iterator[Request]:
        ...

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":
    spider_names = ["grubhub_spider"]

    start_scrapy_crawl(
        spider_names=spider_names,
        max_requests=1,
        output_folder=s.OUTPUT_FOLDER,
    )
