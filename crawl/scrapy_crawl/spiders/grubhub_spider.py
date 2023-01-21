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
    second_section_header = True

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
            callback=self.parse_restaurant,
            # errback=self.handle_errback,
            meta={"dont_merge_cookies": True},
            headers={
                "Cache-Control": "max-age=0",
                "Authorization": f"Bearer {access_token}",
            },
            cb_kwargs={
                "access_token": access_token,
                "restaurant_id": restaurant_id,
            },
        )
        yield next_request

    def parse_restaurant(
        self, response: Response, access_token: str, restaurant_id: str
    ) -> Iterator[Request]:
        restaurant_dict = json.loads(response.body)
        path = "restaurant.name"
        print(f"Restaurant Name: {jmespath.search(path, restaurant_dict)}")
        path = "restaurant.address.street_address"
        print(f"Restaurant Address Line 1: {jmespath.search(path, restaurant_dict)}")
        path = "restaurant.address.locality"
        print(f"Restaurant City: {jmespath.search(path, restaurant_dict)}")
        path = "restaurant.address.region"
        print(f"Restaurant State: {jmespath.search(path, restaurant_dict)}")
        path = "restaurant.rating_bayesian_half_point.rating_value"
        print(f"Restaurant Stars: {jmespath.search(path, restaurant_dict)}")
        path = "restaurant.faceted_rating_data.review_data.valid_count"
        print(f"Restaurant Review Count: {jmespath.search(path, restaurant_dict)}")

        path = (
            '{"Category Name": menu_category_name, '
            '"Item Name": name, '
            '"Item Description": description, '
            '"Item Price": minimum_price_variation.amount, '
            '"": ``}'  # Empty column to store
        )
        path = f"restaurant.menu_category_list[].menu_item_list[].{path}"
        menu_items = jmespath.search(path, restaurant_dict)
        yield from menu_items

        path = "restaurant.menu_category_list[].menu_item_list[].id"
        # TODO: Add verification for menu_item_list_ids (if empty or None)
        menu_item_list_ids = jmespath.search(path, restaurant_dict)
        # Slice is used for testing. See below
        for menu_item_list_id in menu_item_list_ids[:2]:
            next_request = Request(
                url=(
                    f"https://api-gtm.grubhub.com/restaurants/{restaurant_id}"
                    f"/menu_items/{menu_item_list_id}"
                    f"?hideUnavailableMenuItems=true"
                    f"&orderType=standard"
                    f"&version={VERSION}"
                ),
                callback=self.parse,
                # errback=self.handle_errback,
                meta={"dont_merge_cookies": True},
                headers={
                    "Cache-Control": "no-cache",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            yield next_request

    def parse(self, response: Response, **kwargs):
        modifiers_dict = json.loads(response.body)
        path = (
            '{"Modifier Group Name": name, '
            '"Modifier Min": min_choice_options, '
            '"Modifier Max": max_choice_options, '
            '"Option Name": choice_option_list[].description, '
            '"Option Price": choice_option_list[].price.amount}'
        )
        path = f"choice_category_list[].{path}"
        modifier_items = jmespath.search(path, modifiers_dict)

        if self.second_section_header:
            self.second_section_header = False
            # Second section mapping
            yield {
                "Category Name": "Modifier Group Name",
                "Item Name": "Modifier Min",
                "Item Description": "Modifier Max",
                "Item Price": "Option Name",
                "": "Option Price",
            }

        for item in modifier_items:
            for name, price in zip(item["Option Name"], item["Option Price"]):
                # Second section data
                yield {
                    "Category Name": item["Modifier Group Name"],
                    "Item Name": item["Modifier Min"],
                    "Item Description": item["Modifier Max"],
                    "Item Price": name,
                    "": price,
                }


if __name__ == "__main__":
    import project_settings as s
    from crawl.starter import start_scrapy_crawl

    spider_names = ["grubhub_spider"]

    start_scrapy_crawl(
        spider_names=spider_names,
        restaurant_url="https://www.grubhub.com/restaurant/mezeh-optimist-hall-340-e-16th-st-unit-r201-charlotte/2809951",
        output_folder=s.OUTPUT_FOLDER,
    )
