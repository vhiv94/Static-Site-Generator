import re

from typing import Callable
from src.parent_node import ParentNode, DivNode
from src.html_node import HTMLNode
from src.text_node import TextNode, TextType, BlockType
from src.leaf_node import LeafNode

_ExtractLinksFunc = Callable[[str], list[tuple[str, str]]]

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


def markdown_to_html(markdown: str) -> DivNode:
    """Converts markdown to a single RootNode containing the html hierarchy"""
    parents: list[HTMLNode] = []
    blocks = split_markdown_blocks(markdown)
    for block in blocks:
        block_type = get_block_type_from_block(block)
        match block_type:
            case BlockType.PARAGRAPH:
                parents.append(ParentNode("p", text_to_leaf_nodes(block)))
            case BlockType.HEADING:
                count = block.count("#", 0, 7)
                parents.append(
                    ParentNode(f"h{count}", text_to_leaf_nodes(block[count + 1 :]))
                )
            case BlockType.CODE:
                code = block[3:-3]
                language: str = code[: code.find("\n")]
                child: list[HTMLNode] = []
                if not language:
                    child.append(LeafNode("code", code))
                else:
                    child.append(
                        LeafNode(
                            "code",
                            code[len(language) :],
                            {"class": f"language-{language}"},
                        )
                    )
                parents.append(ParentNode("pre", child))
            case BlockType.QUOTE:
                # quote = "\n".join(map(lambda line: line.lstrip(">"), block.split("\n")))
                quote = re.sub(r"(?m)^>\s?", "", block)
                parents.append(ParentNode("blockquote", text_to_leaf_nodes(quote)))
            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                parents.append(_list_to_list_node(block.split("\n"))[0])
            case _:
                raise ValueError("Error: markdown to html: block has no type")    
            

    return DivNode(parents)


def split_markdown_blocks(markdown: str) -> list[str]:
    """Split markdown into blocks separated by exactly one blank line.

    Raises:
        ValueError: If the input contains 3 or more consecutive newlines.
    """
    if re.search(r"\n{3,}", markdown):
        raise ValueError("too much white space in markdown file")
    return markdown.strip().split("\n\n")


def get_block_type_from_block(block: str) -> BlockType:
    """Infer a block type from the block's leading marker."""
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith(("- ", "* ")):
        return BlockType.UNORDERED_LIST
    elif re.match(r"\d+\.\s", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


# def structure_list_nodes(
#     lst: list[str], *, is_ordered: bool = False, start: int | None = None
# ) -> list[HTMLNode]:
#     children: list[HTMLNode] = []
#     for line in lst:
#         if re.match(r"\d+\.\s", line) or line.startswith(("- ", "* ")):
#             children.append(ParentNode("li", text_to_leaf_nodes(line[2:])))
#         else:
#             raise ValueError(
#                 "Error: unordered list to nodes: line isn't formatted properly"
#             )
#     return children


def _list_to_list_node(lines:list[str], *, idx:int=0, depth:int=0) -> tuple[HTMLNode, int]:
    children: list[HTMLNode] = []
    is_ordered: bool | None = None
    while idx < len(lines):
        line = lines[idx]
        indent = len(line) - len(re.sub(r"(?m)^\s+", "", line))

        if indent < depth:
            break # we've returned to the previous depth so return to caller
        if indent > depth:
            # we've stepped deeper into the hierarch
            # if double tab/list starts indented
            if not children:
                raise ValueError("Error: list to nodes: list hierarchy isn't formatted properly")
            # recurse and attatch the return list to the current child
            nested, idx = _list_to_list_node(lines, idx=idx, depth=indent)
            
            # get the children of the last child
            last_li = children[-1]
            li_children = list(last_li.children or [])
            li_children.append(nested)
            last_li.children = li_children
            continue

        # we're at the current depth level
        content = line[depth:]
        match = re.match(r"\d+\.\s", content)
        if match and (is_ordered is None or is_ordered is True):
            is_ordered = True
            children.append(
                ParentNode(
                    "li", text_to_leaf_nodes(re.sub(r"(?m)^\d+\.\s", "", content)), {"value": int(re.sub(r"\.\s", "", match.group()))}
                )
            )
        elif content.startswith(("- ", "* ")) and (is_ordered is None or is_ordered is False):
            is_ordered = False
            children.append(ParentNode("li", text_to_leaf_nodes(content[2:])))
        else:
            raise ValueError(
                "Error: list to list nodes: line isn't formatted properly"
            )
        # finished with the current line, increment index
        idx += 1

    # return up the depth or finished the list
    parent = ParentNode("ol" if is_ordered else "ul", children)
    return parent, idx


def _parse_list_nodes_r(lines:list[str], *, idx:int=0, depth:int=0, is_ordered:bool) -> tuple[list[HTMLNode], int]:
    children = []
    while idx < len(lines):
        line = lines[idx]
        indent = len(line) - len(line.lstrip("\t"))

        if indent < depth:
            break  # return to caller
        if indent > depth:
            # recurse and attach nested list to last <li>
            if not children:
                raise ValueError("nested list without parent item")
            nested, idx = _parse_list_nodes_r(
                lines, idx=idx, depth=depth + 1, is_ordered=is_ordered
            )
            last_li = children[-1]
            li_children = list(last_li.children or [])
            li_children.append(ParentNode("ol" if is_ordered else "ul", nested))
            last_li.children = li_children
            continue

        # indent == depth: parse this line's marker/content
        content = line[depth:]  # remove exactly current-level tabs
        # then validate marker and strip "- "/"* " or r"^\d+\.\s+" accordingly
        if is_ordered and re.match(r"\d+\.\s", content):
            num = re.match(r"\d+", content)
            value_attr: dict[str, str] = {"value": num.group() if num else '0'}
            children.append(
                ParentNode(
                    "li", text_to_leaf_nodes(re.sub(r"(?m)^\d+\.\s", "", content)), value_attr 
                )
            )
        elif content.startswith(("- ", "* ")):
            children.append(ParentNode("li", text_to_leaf_nodes(content[2:])))
        else:
            raise ValueError(
                "Error: unordered list to nodes: line isn't formatted properly"
            )

        idx += 1

    return children, idx


def _validate_prefix(
    value: str,
    error_message: str,
    *,
    lowercase: bool = False,
) -> None:
    """Validate that a URL/path starts with an allowed prefix."""
    candidate = value.lstrip()
    if lowercase:
        candidate = candidate.lower()
    if not candidate.startswith(LINK_PREFIXES):
        raise ValueError(f"Error: text node to leaf node: {error_message}")


def text_node_to_leaf_node(text_node: TextNode) -> LeafNode:
    """Convert a text node to its equivalent leaf-node representation."""
    if text_node.text_type == TextType.LINK:
        url = text_node.url
        if url is None:
            raise ValueError("Error: text node to leaf node: Links need a url")

        _validate_prefix(url, "invalid url", lowercase=True)
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


def extract_links_factory(regex: str) -> _ExtractLinksFunc:
    """Return an extractor function that finds markdown links via regex."""

    def wrapper(text: str) -> list[tuple[str, str]]:
        """Extract all regex matches from input text."""
        return re.findall(regex, text)

    return wrapper


def text_to_leaf_nodes(text: str) -> list[HTMLNode]:
    """Parse inline markdown in text and return rendered leaf nodes."""
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


def _skip_non_plain_or_no_delimiter(
    node: TextNode, out: list[TextNode], delimiter: str | None = None
) -> bool:
    """Append and skip nodes that are non-plain or missing a delimiter."""
    if node.text_type != TextType.PLAIN or (delimiter and delimiter not in node.text):
        out.append(node)
        return True
    return False


def split_nodes_on_links(
    old_nodes: list[TextNode], *, is_url: bool = False
) -> list[TextNode]:
    """Split plain text nodes into plain/link/image nodes."""
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
    """Split plain nodes on a delimiter and type alternating segments."""
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
