from ssl import SSLContext
from types import SimpleNamespace
from typing import Any, Awaitable, Callable, Iterable, Mapping, Optional, Union

from aiohttp import BasicAuth, ClientResponse, ClientTimeout, Fingerprint
from aiohttp.helpers import _SENTINEL
from aiohttp.typedefs import LooseCookies, LooseHeaders, StrOrURL
from scrapy.http import Request


class RequestParser:
    def __init__(self, request: Request) -> None:
        self._request = request
        self._aiohttp_args = request.meta.get("aiohttp_args", {})

    @property
    def method(self) -> str:
        return self._request.method

    @property
    def url(self) -> str:
        return self._request.url

    @property
    def params(self) -> Optional[Mapping[str, str]]:
        return self._aiohttp_args.get("params")

    @property
    def data(self) -> Any:
        return self._request.body

    @property
    def json(self) -> Any:
        return self._aiohttp_args.get("json")

    @property
    def cookies(self) -> Optional[LooseCookies]:
        cookies = self._request.cookies
        if isinstance(cookies, list):
            return {k: v for cookie in cookies for k, v in cookie.items()}

        elif isinstance(cookies, dict):
            return {k: v for k, v in cookies.items()}

        else:
            return {}

    @property
    def headers(self) -> Optional[LooseHeaders]:
        headers = self._request.headers.to_unicode_dict()
        return dict(headers)

    @property
    def skip_auto_headers(self) -> Optional[Iterable[str]]:
        return self._aiohttp_args.get("skip_auto_headers")

    @property
    def auth(self) -> Optional[BasicAuth]:
        return self._aiohttp_args.get("auth")

    @property
    def allow_redirects(self) -> bool:
        return self._aiohttp_args.get("allow_redirects", True)

    @property
    def max_redirects(self) -> int:
        return self._aiohttp_args.get("max_redirects", 10)

    @property
    def compress(self) -> Optional[str]:
        return self._aiohttp_args.get("compress")

    @property
    def chunked(self) -> Optional[bool]:
        return self._aiohttp_args.get("chunked")

    @property
    def expect100(self) -> bool:
        return self._aiohttp_args.get("expect100", False)

    @property
    def raise_for_status(self) -> Union[None, bool, Callable[[ClientResponse], Awaitable[None]]]:
        return self._aiohttp_args.get("raise_for_status")

    @property
    def read_until_eof(self) -> bool:
        return self._aiohttp_args.get("read_until_eof", True)

    @property
    def proxy(self) -> Optional[StrOrURL]:
        return self._request.meta.get("proxy")

    @property
    def proxy_auth(self) -> Optional[BasicAuth]:
        return self._aiohttp_args.get("proxy_auth")

    @property
    def timeout(self) -> Union[ClientTimeout, _SENTINEL]:
        return self._aiohttp_args.get("timeout", _SENTINEL.sentinel)

    @property
    def verify_ssl(self) -> Optional[bool]:
        return self._aiohttp_args.get("verify_ssl")

    @property
    def fingerprint(self) -> Optional[bytes]:
        return self._aiohttp_args.get("fingerprint")

    @property
    def ssl_context(self) -> Optional[SSLContext]:
        return self._aiohttp_args.get("ssl_context")

    @property
    def ssl(self) -> Union[SSLContext, bool, Fingerprint]:
        return self._aiohttp_args.get("ssl", True)

    @property
    def server_hostname(self) -> Optional[str]:
        return self._aiohttp_args.get("server_hostname")

    @property
    def proxy_headers(self) -> Optional[LooseHeaders]:
        return self._aiohttp_args.get("proxy_headers")

    @property
    def trace_request_ctx(self) -> Optional[SimpleNamespace]:
        return self._aiohttp_args.get("trace_request_ctx")

    @property
    def read_bufsize(self) -> Optional[int]:
        return self._aiohttp_args.get("read_bufsize")

    @property
    def auto_decompress(self) -> Optional[bool]:
        return self._aiohttp_args.get("auto_decompress")

    @property
    def max_line_size(self) -> Optional[int]:
        return self._aiohttp_args.get("max_line_size")

    @property
    def max_field_size(self) -> Optional[int]:
        return self._aiohttp_args.get("max_field_size")

    def as_dict(self) -> dict:
        return {
            property_name: getattr(self, property_name)
            for property_name, method in self.__class__.__dict__.items()
            if isinstance(method, property)
        }
