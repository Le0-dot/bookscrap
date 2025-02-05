"""
Defenitions of the protocols used by plugins.
"""

from typing import Protocol, runtime_checkable

from selectolax.parser import HTMLParser


@runtime_checkable
class ParserProvider(Protocol):
    @staticmethod
    def extract_identifier(tree: HTMLParser, url: str) -> str: ...

    @staticmethod
    def extract_title(tree: HTMLParser) -> str: ...

    @staticmethod
    def extract_text(tree: HTMLParser) -> str: ...

    @staticmethod
    def extract_next_page(tree: HTMLParser, url: str) -> str | None: ...


@runtime_checkable
class AsyncHTTPDownloader(Protocol):
    @staticmethod
    async def download(url: str) -> str: ...

    @staticmethod
    async def cleanup() -> None: ...


@runtime_checkable
class AsyncCallback(Protocol):
    @staticmethod
    async def handle_success(identifier: str, title: str, text: str) -> None: ...

    @staticmethod
    async def handle_download_exception(exception: Exception, url: str) -> None: ...

    @staticmethod
    async def handle_parser_exception(exception: Exception, url: str) -> bool: ...
