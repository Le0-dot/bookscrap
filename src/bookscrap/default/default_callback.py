"""
Default callback.
Could be used to save downloaded files.
Skips page if any errors were encountered during parsing.
"""

from sys import stderr

import aiofiles


async def handle_success(identifier: str, title: str, text: str) -> None:
    async with aiofiles.open(
        f"{identifier:03}.txt", encoding="utf-8", mode="w"
    ) as file:
        await file.write(title)
        await file.write("\n")
        await file.write(text)


async def handle_download_exception(exception: Exception, url: str) -> None:
    print(
        f"Encountered error during processing of {url}: {exception}",
        file=stderr,
        flush=True,
    )


async def handle_parser_exception(exception: Exception, url: str) -> bool:
    print(
        f"Encountered error during processing of {url}: {exception}",
        file=stderr,
        flush=True,
    )
    return True
