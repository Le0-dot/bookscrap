"""
Default callback.
Could be used to save downloaded files.
Skips page if any errors were encountered during parsing.
"""

from sys import stderr


def handle_success(title: str, text: str, number: int) -> None:
    with open(f"{number:03d}.txt", encoding="utf-8", mode="w") as file:
        file.writelines([title, "\n", text])


def handle_download_exception(exception: Exception, url: str) -> None:
    print(f"Encountered error during processing of {url}: {exception}", file=stderr)


def handle_parser_exception(exception: Exception, url: str) -> bool:
    print(f"Encountered error during processing of {url}: {exception}", file=stderr)
    return True
