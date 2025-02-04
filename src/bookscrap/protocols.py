"""
Defenitions of the protocols used by plugins.
"""

from typing import Protocol, runtime_checkable

from selectolax.parser import HTMLParser


@runtime_checkable
class ParserProvider(Protocol):
    @staticmethod
    def extract_title(tree: HTMLParser) -> str: ...

    @staticmethod
    def extract_text(tree: HTMLParser) -> str: ...

    @staticmethod
    def extract_next_page(tree: HTMLParser, url: str) -> str | None: ...

    @staticmethod
    def extract_number(tree: HTMLParser, url: str) -> int: ...


@runtime_checkable
class HTTPDownloader(Protocol):
    @staticmethod
    def download(url: str) -> str: ...

    @staticmethod
    def cleanup() -> None: ...


@runtime_checkable
class Callback(Protocol):
    @staticmethod
    def handle_success(title: str, text: str, number: int) -> None: ...

    @staticmethod
    def handle_download_exception(exception: Exception, url: str) -> None: ...

    @staticmethod
    def handle_parser_exception(exception: Exception, url: str) -> bool: ...
