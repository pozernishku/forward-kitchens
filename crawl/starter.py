import logging
import pathlib
from datetime import datetime
from typing import List

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import project_settings as s

logger = logging.getLogger(__name__)
configure_logging()


def get_crawling_output_filename(spider_name: str, output_folder: str) -> str:
    timestamp = datetime.today().strftime("%Y%m%d_%H%M")
    filename = f"{timestamp}__{spider_name}.csv"
    market_name = s.SOURCE_TO_MARKET_MAPPING[spider_name]
    crawl_result_path = pathlib.PurePosixPath(s.ROOT_DIR).joinpath(
        output_folder, market_name, spider_name, filename
    )
    return str(crawl_result_path)


def start_scrapy_crawl(
    spider_names: List[str],
    max_requests: int = s.MAX_REQUESTS,
    output_folder: str = s.OUTPUT_FOLDER,
) -> str:
    assert spider_names is not None
    spider_names = spider_names if isinstance(spider_names, list) else [spider_names]
    # TODO: Log to every single crawl job
    crawl_csv = get_crawling_output_filename(spider_names[0], output_folder)
    # register_all_loggers(crawl_csv)

    scrapy_settings = get_project_settings()
    scrapy_settings.update(
        {"FEEDS": {pathlib.Path(crawl_csv).as_uri(): {"format": "csv"}}}
    )
    process = CrawlerProcess(settings=scrapy_settings)
    for spider_name in spider_names:
        logger.info(f"Starting Scrapy crawl: '{spider_name}' ...")
        process.crawl(spider_name, max_requests=max_requests)
    process.start()

    # if len(spider_names) > 1:
    #     remove_duplicate_rows_in_csv(crawl_csv)
    #     split_quotes_and_prices_data(pathlib.Path(crawl_csv))
    # add_general_info_to_logfile(crawl_csv)
    return crawl_csv
