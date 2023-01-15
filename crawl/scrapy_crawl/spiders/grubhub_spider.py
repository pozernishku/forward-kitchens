import json
import re
from typing import Iterator

import jmespath
from scrapy import Spider
from scrapy.http import Request, Response
from scrapy.utils.project import get_project_settings

BRAND = "GRUBHUB"
CLIENT_ID = "beta_UmWlpstzQSFmocLy3h1UieYcVST"
DEVICE_ID = 1844483276
SCOPE = "anonymous"
VERSION = "4"


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

    # Usage: scrapy crawl grubhub_spider -a restaurant_url="URL"
    # or add restaurant_url="URL" into process.crawl(), see start_scrapy_crawl()
    restaurant_url = ""

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
        auth_dict = json.loads(response.body)
        access_token = jmespath.search("session_handle.access_token", auth_dict)
        url = self.restaurant_url
        restaurant_id = re.sub(r".*/restaurant/.+?/(\d+)/?.*", r"\1", url)
        next_request = Request(
            url=(
                f"https://api-gtm.grubhub.com/restaurants/{restaurant_id}"
                f"?hideChoiceCategories=true"
                f"&version={VERSION}"
                f"&variationId=rtpFreeItems"
                f"&orderType=standard"
                f"&hideUnavailableMenuItems=true"
                f"&hideMenuItems=false"
            ),
            callback=self.parse,
            # errback=self.handle_errback,
            meta={"dont_merge_cookies": True},
            headers={
                "Cache-Control": "max-age=0",
                "Authorization": f"Bearer {access_token}",
            },
            cb_kwargs={
                "access_token": access_token,
            },
        )
        yield next_request

    def parse(self, response, **kwargs):
        pass


if __name__ == "__main__":
    import project_settings as s
    from crawl.starter import start_scrapy_crawl

    spider_names = ["grubhub_spider"]

    start_scrapy_crawl(
        spider_names=spider_names,
        restaurant_url="https://www.grubhub.com/restaurant/mezeh-optimist-hall-340-e-16th-st-unit-r201-charlotte/2809951",
        max_requests=1,
        output_folder=s.OUTPUT_FOLDER,
    )
