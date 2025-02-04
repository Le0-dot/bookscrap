from importlib.metadata import EntryPoint, EntryPoints, entry_points
from typing import NamedTuple, Any
from argparse import ArgumentParser, Namespace

from selectolax.parser import HTMLParser

from .protocols import ParserProvider, HTTPDownloader, Callback


class Plugins(NamedTuple):
    parser_providers: EntryPoints
    http_downloaders: EntryPoints
    callbacks: EntryPoints


def find_plugins() -> Plugins:
    # Setup default plugin implementations
    default_provider = EntryPoint(
        name="default_provider",
        group="bookscrap.parser-provider",
        value=f"{__package__}.default.default_provider",
    )
    default_downloader = EntryPoint(
        name="default_downloader",
        group="bookscrap.http-downloader",
        value=f"{__package__}.default.default_downloader",
    )
    default_callback = EntryPoint(
        name="default_callback",
        group="bookscrap.callback",
        value=f"{__package__}.default.default_callback",
    )

    # Find all installed plugins and append default ones
    parser_providers = EntryPoints(
        (*entry_points(group="bookscrap.parser-provider"), default_provider)
    )
    http_downloaders = EntryPoints(
        (*entry_points(group="bookscrap.http-downloader"), default_downloader)
    )
    callbacks = EntryPoints(
        (*entry_points(group="bookscrap.callback"), default_callback)
    )

    return Plugins(parser_providers, http_downloaders, callbacks)


def check_plugin[T](module: Any, protocol: type[T]) -> T:
    if not isinstance(module, protocol):
        raise RuntimeError(
            f"{module.__name__} does not conform to {protocol.__name__} protocol"
        )
    return module


def download_pages(
    start_url: str,
    parser_provider: ParserProvider,
    http_downloader: HTTPDownloader,
    callback: Callback,
) -> None:
    url: str | None = start_url
    while url is not None:
        try:
            html_response = http_downloader.download(url)
        except Exception as exception:
            callback.handle_download_exception(exception, url)
            return

        tree = HTMLParser(html_response)

        try:
            title = parser_provider.extract_title(tree)
            text = parser_provider.extract_text(tree)
            new_url = parser_provider.extract_next_page(tree, url)
            number = parser_provider.extract_number(tree, url)

            callback.handle_success(title, text, number)
            url = new_url
        except Exception as exception:
            if not callback.handle_parser_exception(exception, url):
                return

def parse_agruments() -> Namespace:
    parser = ArgumentParser()

    parser.prog = "bookscrap"

    parser.add_argument("--parser-provider", default="default_provider")
    parser.add_argument("--http-downloader", default="default_downloader")
    parser.add_argument("--callback", default="default_callback")
    parser.add_argument("url")

    return parser.parse_args()


def main() -> None:
    args = parse_agruments()
    plugins = find_plugins()

    module = plugins.parser_providers[args.parser_provider].load()
    provider = check_plugin(module, ParserProvider)

    module = plugins.http_downloaders[args.http_downloader].load()
    downloader = check_plugin(module, HTTPDownloader)

    module = plugins.callbacks[args.callback].load()
    callback = check_plugin(module, Callback)

    download_pages(args.url, provider, downloader, callback)

if __name__ == "__main__":
    main()
