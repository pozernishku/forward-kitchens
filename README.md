# forward-kitchens
Reverse engineering [home task](https://forwardkitchens.notion.site/forwardkitchens/Reverse-Engineering-Take-Home-Assignment-a15843a2763f4bc6a9ee554f57ff2720)
from Forward Kitchens

# Install
1. Run `git clone https://github.com/pozernishku/forward-kitchens.git`
2. Go to project directory `cd forward-kitchens`
3. Create an environment file `.env` with the following secrets (ask [me](https://t.me/zackushka))
   - `SMARTPROXY_USER=...`
   - `SMARTPROXY_PASSWORD=...`
4. Activate environment `poetry shell` (requires [poetry to be installed](https://python-poetry.org/docs/#installation))
5. To install project dependencies, run `poetry install --no-root`

# Run
1. Go to the `crawl` directory of the project `cd crawl`
2. Run `scrapy crawl grubhub_spider --nolog -a restaurant_url="URL" -O ../crawl_output/us/grubhub_spider/grubhub_spider__output.csv`
   - Use any [restaurant URL](https://www.grubhub.com/restaurant/mezeh-optimist-hall-340-e-16th-st-unit-r201-charlotte/2809951) in `-a restaurant_url="URL"`
   - Optionally, add `--logfile ../crawl_output/us/grubhub_spider/grubhub_spider__output.log`
3. Check the output in `grubhub_spider__output.csv`
4. Alternatively, it's possible to start a crawl from a python file, see `forward-kitchens/crawl/scrapy_crawl/spiders/grubhub_spider.py`
   - Check this section `if __name__ == "__main__":`

# Details
I used asynchronous [Scrapy framework](https://docs.scrapy.org/en/latest/) to complete
this task. Scrapy has a good [architecture](https://docs.scrapy.org/en/latest/topics/architecture.html)
and contains a lot of features designed for crawling, which is why I chose it. Scrapy is
based on [twisted](https://twisted.org/), but modern [asyncio](https://docs.scrapy.org/en/latest/topics/asyncio.html)
is also supported.

[Paid proxies](https://smartproxy.com/) (US) were used to bypass
[grubhub.com](https://grubhub.com/) from Ukraine.

For reconnaissance, I used [mitmproxy](https://mitmproxy.org/) and [Burp Suite](https://portswigger.net/burp).

With Scrapy, it's easy to redesign the project for scalability (to crawl hundreds of
URLs). It is possible to rewrite the `start_requests()` to read in URLs (or restaurant
IDs) from a file or other source. To increase requests concurrency use
`CONCURRENT_REQUESTS` (16 by default) setting or related. Also, the [AutoThrottle extension](https://docs.scrapy.org/en/latest/topics/autothrottle.html)
can help with crawling speed. As an option, it is possible to spread the load and make a
[distributed crawl](https://docs.scrapy.org/en/latest/topics/practices.html#distributed-crawls).

It's always good to have a scheduled test job (runs daily at 8:00 am, for example) which
will run spiders to test them. Logs will be saved and in case of failures the message
will be sent to Slack or somewhere else. Also, Kibana might be an option here.
