"""
Main logic of appliction
"""

import asyncio

from selectolax.parser import HTMLParser

from .plugins.protocols import AsyncCallback, AsyncHTTPDownloader, ParserProvider


async def run(
    start_url: str,
    parser_provider: ParserProvider,
    http_downloader: AsyncHTTPDownloader,
    callback: AsyncCallback,
    timeout_seconds: float,
) -> None:
    next_url: str | None = start_url
    while next_url is not None:
        url = next_url
        try:
            html_response = await http_downloader.download(url)
        except Exception as exception:
            await callback.handle_download_exception(exception, url)
            return

        tree = HTMLParser(html_response)

        try:
            identifier = parser_provider.extract_identifier(tree, url)
            title = parser_provider.extract_title(tree)
            text = parser_provider.extract_text(tree)
            next_url = parser_provider.extract_next_page(tree, url)
            await callback.handle_success(identifier, title, text)
        except Exception as exception:
            to_continue = await callback.handle_parser_exception(exception, url)
            if not to_continue:
                return

        await asyncio.sleep(timeout_seconds)
