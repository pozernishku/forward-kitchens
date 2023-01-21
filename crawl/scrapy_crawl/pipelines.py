# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyCrawlPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(adapter.get("Category Name"), str):
            adapter["Category Name"] = adapter["Category Name"].strip()
        if isinstance(adapter.get("Item Name"), str):
            adapter["Item Name"] = adapter["Item Name"].strip()
        if isinstance(adapter.get("Item Description"), str):
            # TODO: Get rid of multi-lines
            adapter["Item Description"] = adapter["Item Description"].strip()
        if isinstance(adapter.get("Item Price"), int):
            adapter["Item Price"] = adapter["Item Price"] / 100
        elif isinstance(adapter.get("Item Price"), str):
            adapter["Item Price"] = adapter["Item Price"].strip()
        if isinstance(adapter.get(""), int):
            adapter[""] = adapter[""] / 100  # Option Price
        return item
