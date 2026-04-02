import pytest

from converters import split_nodes_delimiter, text_node_to_leaf_node
from text_node import TextNode, TextType


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com",
        "/docs/page",
        "./relative/path",
        "../up/one",
        "#heading-1",
        "mailto:user@example.com",
    ],
)
def test_text_node_to_leaf_node_anchor_accepts_valid_url_prefixes(url: str) -> None:
    node = TextNode("link text", TextType.ANCHOR_TEXT, url)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == "a"
    assert leaf_node.value == "link text"
    assert leaf_node.props == {"href": url}


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "javascript:alert(1)",
        "www.example.com",
        "example.com/path",
    ],
)
def test_text_node_to_leaf_node_anchor_rejects_invalid_url_prefixes(url: str) -> None:
    node = TextNode("link text", TextType.ANCHOR_TEXT, url)

    with pytest.raises(ValueError, match="invalid url"):
        text_node_to_leaf_node(node)


def test_text_node_to_leaf_node_anchor_requires_url() -> None:
    node = TextNode("link text", TextType.ANCHOR_TEXT)

    with pytest.raises(ValueError, match="Links need a url"):
        text_node_to_leaf_node(node)


@pytest.mark.parametrize("url", ["/image.png", "./assets/image.png", "../images/photo.jpg"])
def test_text_node_to_leaf_node_alt_accepts_valid_path_prefixes(url: str) -> None:
    node = TextNode("hero image", TextType.ALT_TEXT, url)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == "img"
    assert leaf_node.value is None
    assert leaf_node.props == {"src": url, "alt": "hero image"}


@pytest.mark.parametrize(
    "url",
    [
        "https://cdn.example.com/image.png",
        "images/photo.jpg",
        "C:/images/photo.jpg",
    ],
)
def test_text_node_to_leaf_node_alt_rejects_invalid_path_prefixes(url: str) -> None:
    node = TextNode("hero image", TextType.ALT_TEXT, url)

    with pytest.raises(ValueError, match="invalid path to image"):
        text_node_to_leaf_node(node)


def test_text_node_to_leaf_node_alt_requires_url() -> None:
    node = TextNode("hero image", TextType.ALT_TEXT)

    with pytest.raises(ValueError, match="Images need a url"):
        text_node_to_leaf_node(node)


@pytest.mark.parametrize(
    ("text_type", "expected_tag"),
    [
        (TextType.PLAIN_TEXT, None),
        (TextType.BOLD_TEXT, "b"),
        (TextType.ITALIC_TEXT, "i"),
        (TextType.CODE_TEXT, "code"),
    ],
)
def test_text_node_to_leaf_node_non_link_or_image_types_return_plain_leafnode(
    text_type: TextType, expected_tag: str | None
) -> None:
    node = TextNode("plain value", text_type)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == expected_tag
    assert leaf_node.value == "plain value"
    assert leaf_node.props is None


def test_text_node_to_leaf_node_anchor_allows_leading_whitespace_and_mixed_case_scheme() -> None:
    node = TextNode("link text", TextType.ANCHOR_TEXT, "   HtTpS://Boot.Dev/path")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.props == {"href": "   HtTpS://Boot.Dev/path"}


def test_text_node_to_leaf_node_anchor_preserves_original_href_value() -> None:
    node = TextNode("link text", TextType.ANCHOR_TEXT, "  HTTPS://Boot.Dev")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.props == {"href": "  HTTPS://Boot.Dev"}


def test_text_node_to_leaf_node_alt_preserves_original_src_and_alt_values() -> None:
    node = TextNode("Profile image", TextType.ALT_TEXT, "   ../assets/pic.png")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.props == {"src": "   ../assets/pic.png", "alt": "Profile image"}


def test_split_nodes_delimiter_returns_original_plain_node_when_delimiter_missing() -> None:
    nodes = [TextNode("plain text only", TextType.PLAIN_TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [TextNode("plain text only", TextType.PLAIN_TEXT)]


def test_split_nodes_delimiter_splits_plain_text_into_alternating_types() -> None:
    nodes = [TextNode("start **bold** end", TextType.PLAIN_TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [
        TextNode("start ", TextType.PLAIN_TEXT),
        TextNode("bold", TextType.BOLD_TEXT),
        TextNode(" end", TextType.PLAIN_TEXT),
    ]


def test_split_nodes_delimiter_does_not_split_non_plain_nodes() -> None:
    nodes = [TextNode("**not split**", TextType.CODE_TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [TextNode("**not split**", TextType.CODE_TEXT)]


def test_split_nodes_delimiter_drops_leading_empty_split_segment() -> None:
    nodes = [TextNode("**bold** tail", TextType.PLAIN_TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [
        TextNode("bold", TextType.BOLD_TEXT),
        TextNode(" tail", TextType.PLAIN_TEXT),
    ]


def test_split_nodes_delimiter_drops_trailing_empty_split_segment() -> None:
    nodes = [TextNode("head **bold**", TextType.PLAIN_TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [
        TextNode("head ", TextType.PLAIN_TEXT),
        TextNode("bold", TextType.BOLD_TEXT),
    ]


def test_split_nodes_delimiter_preserves_order_in_mixed_plain_and_non_plain_nodes() -> None:
    nodes = [
        TextNode("alpha **beta**", TextType.PLAIN_TEXT),
        TextNode("**leave me**", TextType.CODE_TEXT),
        TextNode("gamma **delta** epsilon", TextType.PLAIN_TEXT),
    ]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    assert result == [
        TextNode("alpha ", TextType.PLAIN_TEXT),
        TextNode("beta", TextType.BOLD_TEXT),
        TextNode("**leave me**", TextType.CODE_TEXT),
        TextNode("gamma ", TextType.PLAIN_TEXT),
        TextNode("delta", TextType.BOLD_TEXT),
        TextNode(" epsilon", TextType.PLAIN_TEXT),
    ]
