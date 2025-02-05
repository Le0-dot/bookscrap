"""
Default http downloader.
Could be used in simple cases, where there is no anti-bot protection.
"""

from curl_cffi.requests import AsyncSession

session = AsyncSession(impersonate="chrome")


async def download(url: str) -> str:
    response = await session.get(url)
    return response.text


async def cleanup() -> None:
    await session.close()
