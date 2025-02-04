from importlib.metadata import EntryPoint, EntryPoints, entry_points
from selectolax.parser import HTMLParser

from .protocols import ParserProvider, HTTPDownloader, Callback

# Setup default provider and downloader
default_provider = EntryPoint(
    name="default_provider",
    group="bookscrap.parser-provider",
    value="default.default_provider",
)
default_downloader = EntryPoint(
    name="default_downloader",
    group="bookscrap.http_downloader",
    value="default.default_downloader",
)
default_callback = EntryPoint(
    name="default_callback",
    group="bookscrap.callback",
    value="default.default_callback",
)

# Find all installed PraserProviders and HTTPDownloaders and append default ones
parser_providers = EntryPoints(
    (*entry_points(group="bookscrap.parser-provider"), default_provider)
)
http_downloaders = EntryPoints(
    (*entry_points(group="bookscrap.http-downloader"), default_downloader)
)
callbacks = EntryPoints((*entry_points(group="bookscrap.callback"), default_callback))

selected_provider = "default_provider"
selected_downloader = "default_downloader"
selected_callback = "default_callback"

# Select provider and downloader
provider = parser_providers[selected_provider].load()
downloader = http_downloaders[selected_downloader].load()
callback = callbacks[selected_callback].load()

# Check for protocol conformation
if not isinstance(provider, ParserProvider):
    raise RuntimeError(
        f"{selected_provider} does not conform to ParserProvider protocol"
    )

if not isinstance(downloader, HTTPDownloader):
    raise RuntimeError(
        f"{selected_downloader} does not conform to HTTPDownloader protocol"
    )

if not isinstance(callback, Callback):
    raise RuntimeError(f"{selected_callback} does not conform to Callback protocol")

# Download all available pages
url: str | None = "https://www.fanmtl.com/novel/doomsday-jigsaw-game_1.html"

while url is not None:
    try:
        html_response = downloader.download(url)
    except Exception as exception:
        # Handle exception and stop execution
        callback.handle_download_exception(exception, url)
        break

    tree = HTMLParser(html_response)

    try:
        title = provider.extract_title(tree)
        text = provider.extract_text(tree)
        new_url = provider.extract_next_page(tree, url)
        number = provider.extract_number(tree, url)

        callback.handle_success(title, text, number)
        url = new_url
    except Exception as exception:
        # Handle exception and possibly stop execution or skip current page
        if not callback.handle_parser_exception(exception, url):
            break
