# scrapy-aiohttp-downloader

[![version](https://img.shields.io/pypi/v/scrapy-aiohttp-downloader.svg)](https://pypi.python.org/pypi/scrapy-aiohttp-downloader)

`scrapy-aiohttp-downloader` is a Scrapy download handler. 

## Installation

```
pip install scrapy-aiohttp-downloader
```

## Activation

Replace the default `http` and/or `https` Download Handlers through [`DOWNLOAD_HANDLERS`](https://docs.scrapy.org/en/latest/topics/settings.html#download-handlers)

```python
DOWNLOAD_HANDLERS = {
    "http": "scrapy_aiohttp_downloader.AioHTTPDownloadHandler",
    "https": "scrapy_aiohttp_downloader.AioHTTPDownloadHandler",
}
```

Also, be sure to [install the asyncio-based Twisted reactor](https://docs.scrapy.org/en/latest/topics/asyncio.html#installing-the-asyncio-reactor):

```python
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
```

## Basic usage

Set the `aiohttp` [Request.meta](https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request.meta) key to download a request using `aiohttp`:

```python
import scrapy


class AioHTTPSpider(scrapy.Spider):
    name = "spider"
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_aiohttp_downloader.AioHTTPDownloadHandler",
            "https": "scrapy_aiohttp_downloader.AioHTTPDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://example.com/",
            meta={"aiohttp": True},
        )
```
