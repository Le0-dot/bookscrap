"""
Small application to scrape books from internet by utilization of plugin system.
"""

import asyncio
from argparse import ArgumentParser, Namespace

from selectolax.parser import HTMLParser

from .plugins.manager import PluginManager
from .plugins.protocols import AsyncCallback, AsyncHTTPDownloader, ParserProvider


async def download_pages(
    start_url: str,
    parser_provider: ParserProvider,
    http_downloader: AsyncHTTPDownloader,
    callback: AsyncCallback,
    timeout_seconds: float,
) -> None:
    url: str | None = start_url
    while url is not None:
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
            new_url = parser_provider.extract_next_page(tree, url)

            await callback.handle_success(identifier, title, text)
            url = new_url
        except Exception as exception:
            to_continue = await callback.handle_parser_exception(exception, url)
            if not to_continue:
                return

        await asyncio.sleep(timeout_seconds)


def parse_agruments() -> Namespace:
    parser = ArgumentParser()

    parser.prog = "bookscrap"

    parser.add_argument(
        "--parser-provider",
        default="default_provider",
        help="name of the plugin with parser provider",
    )
    parser.add_argument(
        "--http-downloader",
        default="default_downloader",
        help="name of the plugin with http downloader",
    )
    parser.add_argument(
        "--callback",
        default="default_callback",
        help="name of the plugin with callback",
    )
    parser.add_argument(
        "--timeout",
        default=3,
        type=float,
        help="timeout in seconds for stop between processing the pages",
    )
    parser.add_argument("url")

    return parser.parse_args()


def main() -> None:
    args = parse_agruments()
    plugin_manager = PluginManager()

    provider = plugin_manager.load(ParserProvider, args.parser_provider)
    downloader = plugin_manager.load(AsyncHTTPDownloader, args.http_downloader)
    callback = plugin_manager.load(AsyncCallback, args.callback)

    asyncio.run(download_pages(args.url, provider, downloader, callback, args.timeout))
