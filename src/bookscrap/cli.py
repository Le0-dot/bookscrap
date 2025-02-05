"""
Small application to scrape books from internet by utilization of plugin system.
"""

import asyncio
from argparse import ArgumentParser, Namespace

from .plugins.manager import PluginManager
from .plugins.protocols import AsyncCallback, AsyncHTTPDownloader, ParserProvider
from .runner import run


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
    parser.add_argument("url", help="url of the first page with the book")

    return parser.parse_args()


def main() -> None:
    args = parse_agruments()
    plugin_manager = PluginManager()

    provider = plugin_manager.load(ParserProvider, args.parser_provider)
    downloader = plugin_manager.load(AsyncHTTPDownloader, args.http_downloader)
    callback = plugin_manager.load(AsyncCallback, args.callback)

    asyncio.run(run(args.url, provider, downloader, callback, args.timeout))
