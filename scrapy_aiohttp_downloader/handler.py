from typing import Optional, Type, TypeVar

from aiohttp import ClientSession
from scrapy import signals
from scrapy.core.downloader.handlers.http import HTTPDownloadHandler
from scrapy.crawler import Crawler
from scrapy.http import Headers, Request, Response
from scrapy.responsetypes import responsetypes
from scrapy.spiders import Spider
from scrapy.utils.defer import deferred_f_from_coro_f, deferred_from_coro
from scrapy.utils.reactor import verify_installed_reactor
from twisted.internet.defer import Deferred

from scrapy_aiohttp_downloader.parser import RequestParser

AioHTTPHandler = TypeVar("AioHTTPHandler", bound="AioHTTPDownloadHandler")


class AioHTTPDownloadHandler(HTTPDownloadHandler):
    def __init__(self, crawler) -> None:
        settings = crawler.settings
        super().__init__(settings=settings, crawler=crawler)

        verify_installed_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
        crawler.signals.connect(self._engine_started, signals.engine_started)

        self.client: Optional[ClientSession] = None

    @classmethod
    def from_crawler(cls: Type[AioHTTPHandler], crawler: Crawler) -> AioHTTPHandler:
        return cls(crawler)

    @deferred_f_from_coro_f
    async def _engine_started(self, signal, sender) -> None:
        self.client = await ClientSession().__aenter__()

    def download_request(self, request: Request, spider: Spider) -> Deferred:
        if request.meta.get("aiohttp"):
            return deferred_from_coro(self._download_request(request, spider))

        return super().download_request(request, spider)

    async def _download_request(self, request: Request, spider: Spider) -> Response:
        response = await self.client.request(**RequestParser(request).as_dict())  # type: ignore

        headers = Headers(response.headers)
        headers.pop("Content-Encoding", None)

        body = await response.read()
        respcls = responsetypes.from_args(
            headers=headers,
            url=str(response.url),
            body=body,
        )

        return respcls(
            url=str(response.url),
            status=response.status,
            headers=headers,
            body=body,
            flags=["aiohttp"],
            request=request,
        )

    def close(self):  # type: ignore
        yield self._close()
        yield super().close()

    @deferred_f_from_coro_f
    async def _close(self) -> None:
        await self.client.__aexit__()  # type: ignore
