from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
from twisted.web.client import HTTPConnectionPool


class RotatingProxiesDownloadHandler(HTTPDownloadHandler):
    """Solves the problem related to https proxies rotation.
    https://github.com/scrapy/scrapy/issues/1807#issuecomment-199099063
    """

    def __init__(self, settings, crawler):
        super().__init__(settings, crawler)
        from twisted.internet import reactor

        self._pool = HTTPConnectionPool(reactor, persistent=False)
