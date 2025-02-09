"""
Default parser provider.
Should only be used as reference for writing custom providers.
"""

from re import search

from selectolax.parser import HTMLParser


def extract_identifier(tree: HTMLParser, _: str) -> str:
    if (match := search(r"(\d+)", extract_title(tree))) is None:
        return "None"
    return match.group()


def extract_title(tree: HTMLParser) -> str:
    return tree.css_first("h1").text()


def extract_text(tree: HTMLParser) -> str:
    return "\n".join(node.text() for node in tree.css("p"))


def extract_next_page(tree: HTMLParser, _: str) -> str | None:
    return tree.css_first("a.next").attributes["href"]
