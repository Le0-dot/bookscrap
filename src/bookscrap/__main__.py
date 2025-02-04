from importlib.metadata import EntryPoint, EntryPoints, entry_points
from selectolax.parser import HTMLParser

from .protocols import ParserProvider, HTTPDownloader

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

# Find all installed PraserProviders and HTTPDownloaders and append default ones
parser_providers = EntryPoints(
    (*entry_points(group="bookscrap.parser-provider"), default_provider)
)
http_downloaders = EntryPoints(
    (*entry_points(group="bookscrap.http-downloader"), default_downloader)
)

selected_provider = "default_provider"
selected_downloader = "default_downloader"

# Select provider and downloader
provider = parser_providers[selected_provider].load()
downloader = http_downloaders[selected_downloader].load()

# Check for protocol conformation
if not isinstance(provider, ParserProvider):
    raise RuntimeError(
        f"{selected_provider} does not conform to ParserProvider protocol"
    )

if not isinstance(downloader, HTTPDownloader):
    raise RuntimeError(
        f"{selected_downloader} does not conform to HTTPDownloader protocol"
    )

# Download all available pages
url: str | None = "https://www.fanmtl.com/novel/doomsday-jigsaw-game_1.html"

while url is not None:
    html_response = downloader.download(url)

    tree = HTMLParser(html_response)

    title = provider.extract_title(tree)
    text = provider.extract_text(tree)
    number = provider.extract_number(tree, url)
    url = provider.extract_next_page(tree, url)

    # TODO: Save page or call some kind of callback
    print(title, number)
