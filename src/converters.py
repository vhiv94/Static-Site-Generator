import re

from typing import Callable

from text_node import TextNode, TextType

# from parent_node import ParentNode
from leaf_node import LeafNode

extractLinksfunc = Callable[[str], list[tuple[str, str]]]

LINK_PREFIXES = ("http://", "https://", "/", "./", "../", "#", "mailto:")
IMAGE_PATH_PREFIXES = ("/", "./", "../")

LINK_TARGET = (
    r"(?:https?://[^)\s]+|/[^)\s]*|\./[^)\s]*|\.\./[^)\s]*|#[^)\s]+|mailto:[^)\s]+)"
)
URL_REGEX = rf"\[([^\]]+)\]\(({LINK_TARGET})\)"
IMAGE_REGEX = r"!\[([^\]]+)\]\(((?:/|\./|\.\./)[^)\s]*)\)"


def _require_url(url: str | None, error_message: str) -> str:
    if url is None:
        raise ValueError(error_message)
    return url


def _validate_prefix(
    value: str,
    prefixes: tuple[str, ...],
    error_message: str,
    *,
    lowercase: bool = False,
) -> None:
    candidate = value.lstrip()
    if lowercase:
        candidate = candidate.lower()
    if not candidate.startswith(prefixes):
        raise ValueError(error_message)


def text_node_to_leaf_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.ANCHOR_TEXT:
        url = _require_url(
            text_node.url, "Error: text node to leaf node: Links need a url"
        )
        _validate_prefix(
            url,
            LINK_PREFIXES,
            "Error: text node to leaf node: invalid url",
            lowercase=True,
        )
        return LeafNode(text_node.text_type.value, text_node.text, {"href": url})

    if text_node.text_type == TextType.ALT_TEXT:
        url = _require_url(
            text_node.url, "Error: text node to leaf node: Images need a url"
        )
        _validate_prefix(
            url,
            IMAGE_PATH_PREFIXES,
            "Error: text node to leaf node: invalid path to image",
        )
        return LeafNode(
            text_node.text_type.value, None, {"src": url, "alt": text_node.text}
        )

    return LeafNode(text_node.text_type.value, text_node.text)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception("Error: split nodes delimiter: Invalid Markdown syntax")

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            part_type = TextType.PLAIN_TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, part_type))

    return new_nodes


def extract_links_factory(regex: str) -> extractLinksfunc:
    def wrapper(text: str) -> list[tuple[str, str]]:
        return re.findall(regex, text)

    return wrapper


extract_markdown_links = extract_links_factory(URL_REGEX)
extract_markdown_images = extract_links_factory(IMAGE_REGEX)
