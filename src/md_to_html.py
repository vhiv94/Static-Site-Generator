import re

from typing import Callable
from text_node import TextNode, TextType
from leaf_node import LeafNode

extractLinksfunc = Callable[[str], list[tuple[str, str]]]

DELIMITERS = [
    ("`", TextType.CODE),
    ("**", TextType.BOLD),
    ("_", TextType.ITALIC),
]

LINK_PREFIXES = ("http://", "https://", "/", "./", "../", "#", "mailto:")
IMAGE_PATH_PREFIXES = ("/", "./", "../")

LINK_TARGET = (
    r"(?:https?://[^)\s]+|/[^)\s]*|\./[^)\s]*|\.\./[^)\s]*|#[^)\s]+|mailto:[^)\s]+)"
)
URL_REGEX = rf"\[([^\]]+)\]\(({LINK_TARGET})\)"
IMAGE_REGEX = rf"!\[([^\]]+)\]\(({LINK_TARGET})\)"


def _validate_prefix(
    value: str,
    error_message: str,
    *,
    lowercase: bool = False,
) -> None:
    candidate = value.lstrip()
    if lowercase:
        candidate = candidate.lower()
    if not candidate.startswith(LINK_PREFIXES):
        raise ValueError(f"Error: text node to leaf node: {error_message}")


def text_node_to_leaf_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.LINK:
        url = text_node.url
        if url is None:
            raise ValueError("Error: text node to leaf node: Links need a url")

        _validate_prefix(
            url,
            "invalid url",
            lowercase=True,
        )
        return LeafNode(text_node.text_type.value, text_node.text, {"href": url})

    if text_node.text_type == TextType.IMAGE:
        url = text_node.url
        if url is None:
            raise ValueError("Error: text node to leaf node: invalid path to image")

        _validate_prefix(url, "ivalid path")
        return LeafNode(
            text_node.text_type.value, None, {"src": url, "alt": text_node.text}
        )

    return LeafNode(text_node.text_type.value, text_node.text)


def extract_links_factory(regex: str) -> extractLinksfunc:
    def wrapper(text: str) -> list[tuple[str, str]]:
        return re.findall(regex, text)

    return wrapper


def _skip_non_plain_or_no_delimiter(
    node: TextNode, out: list[TextNode], delimiter: str | None = None
) -> bool:
    if node.text_type != TextType.PLAIN or (delimiter and delimiter not in node.text):
        out.append(node)
        return True
    return False


def split_nodes_on_links(
    old_nodes: list[TextNode], *, is_url: bool = False
) -> list[TextNode]:
    extract_links = extract_links_factory(URL_REGEX if is_url else IMAGE_REGEX)

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if _skip_non_plain_or_no_delimiter(node, new_nodes):
            continue

        links = extract_links(node.text)
        old_text_lst = [node.text]
        for a_text, link in links:
            # remove the link from the original text
            old_text_lst = old_text_lst[0].split(
                f"{'' if is_url else '!'}[{a_text}]({link})", 1
            )

            # add the first/next part of the original text
            new_nodes.append(TextNode(old_text_lst[0], TextType.PLAIN))
            del old_text_lst[0]

            # add the link
            text_type = TextType.LINK if is_url else TextType.IMAGE
            new_nodes.append(TextNode(a_text, text_type, link))

        # add the final part of the orignal text or all of it if there were no links
        if old_text_lst[0]:
            new_nodes.append(TextNode(old_text_lst[0], TextType.PLAIN))

    # do it all again, but for urls
    if not is_url:
        new_nodes = split_nodes_on_links(new_nodes.copy(), is_url=True)
    return new_nodes


def split_nodes_on_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if _skip_non_plain_or_no_delimiter(node, new_nodes, delimiter):
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception("Error: split nodes delimiter: Invalid Markdown syntax")

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            part_type = TextType.PLAIN if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, part_type))

    return new_nodes


def text_to_leaf_nodes(text: str) -> list[LeafNode]:
    initial_node = [TextNode(text, TextType.PLAIN)]
    link_nodes = split_nodes_on_links(initial_node)

    # delimit code snippets and bold and italic text
    text_nodes: list[TextNode] = []
    for node in link_nodes:
        # skip non plain text nodes
        if _skip_non_plain_or_no_delimiter(node, text_nodes):
            continue

        # determine delimiters to use
        delimiters = []
        for delimiter, text_type in DELIMITERS:
            if delimiter in node.text:
                delimiters.append((delimiter, text_type))

        # skip if no delimiters present
        if len(delimiters) == 0:
            text_nodes.append(node)
            continue

        # split on each delimiter
        new_nodes: list[TextNode] = [node]
        for delimiter, text_type in delimiters:
            new_nodes = split_nodes_on_delimiter(new_nodes, delimiter, text_type)
        text_nodes.extend(new_nodes)

    # convert to leaf nodes and return
    return list(map(lambda node: text_node_to_leaf_node(node), text_nodes))


def split_markdown_blocks(markdown: str) -> list[str]:
    if re.search(r"\n{3,9}", markdown):
        raise ValueError("too much white space in markdown file")
    return markdown.strip().split("\n\n")
