"""
A module with plugin manager, that handles importing and checking of plugins
"""

from importlib.metadata import EntryPoint, EntryPoints, entry_points

from .protocols import AsyncCallback, AsyncHTTPDownloader, ParserProvider


class PluginManager:
    def __init__(self) -> None:
        self.__plugins = {
            protocol: self.__find_plugins(protocol) for protocol in self.config
        }

    def load[T](self, protocol: type[T], name: str) -> T:
        module = self.__plugins[protocol][name].load()
        if isinstance(module, protocol):
            return module

        raise RuntimeError(
            f"{module.__name__} does not conform to {protocol.__name__} protocol"
        )

    @property
    def config(self) -> dict[type, str]:
        return {
            ParserProvider: "bookscrap.parser_provider",
            AsyncHTTPDownloader: "bookscrap.http_downloader",
            AsyncCallback: "bookscrap.callback",
        }

    @property
    def defaults(self) -> dict[type, EntryPoint]:
        return {
            ParserProvider: EntryPoint(
                name="default_provider",
                group=self.config[ParserProvider],
                value=f"{__package__}.defaults.default_provider",
            ),
            AsyncHTTPDownloader: EntryPoint(
                name="default_downloader",
                group=self.config[AsyncHTTPDownloader],
                value=f"{__package__}.defaults.default_downloader",
            ),
            AsyncCallback: EntryPoint(
                name="default_callback",
                group=self.config[AsyncCallback],
                value=f"{__package__}.defaults.default_callback",
            ),
        }

    def __find_plugins(self, protocol: type):
        return EntryPoints(
            (*entry_points(group=self.config[protocol]), self.defaults[protocol])
        )
