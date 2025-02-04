"""
Default http downloader.
Could be used in simple cases, where there is no anti-bot protection.
"""

from curl_cffi.requests import Session

session = Session(impersonate="chrome")


def download(url: str) -> str:
    return session.get(url).text

def cleanup() -> None:
    session.close()
