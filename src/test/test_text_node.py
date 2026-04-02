from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from converters import text_node_to_leaf_node
from text_node import TextNode, TextType


@pytest.mark.parametrize("text_type", list(TextType))
def test_text_nodes_with_same_fields_are_equal(text_type: TextType) -> None:
    node1 = TextNode("test", text_type)
    node2 = TextNode("test", text_type)
    assert node1 == node2


def test_text_nodes_with_same_url_are_equal() -> None:
    node1 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    assert node1 == node2


def test_text_nodes_with_different_text_types_are_not_equal() -> None:
    node1 = TextNode("test", TextType.PLAIN_TEXT)
    node2 = TextNode("test", TextType.BOLD_TEXT)
    assert node1 != node2


def test_text_nodes_with_different_text_are_not_equal() -> None:
    node1 = TextNode("test", TextType.PLAIN_TEXT)
    node2 = TextNode("oops", TextType.PLAIN_TEXT)
    assert node1 != node2


def test_text_nodes_with_different_urls_are_not_equal() -> None:
    node1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.ANCHOR_TEXT, "https//:test.com")
    assert node1 != node2


def test_text_nodes_with_url_and_none_url_are_not_equal() -> None:
    node1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.ANCHOR_TEXT)
    assert node1 != node2


def test_text_nodes_with_empty_text_are_equal() -> None:
    node1 = TextNode("", TextType.PLAIN_TEXT)
    node2 = TextNode("", TextType.PLAIN_TEXT)
    assert node1 == node2


def test_repr_formats_text_node_fields() -> None:
    node = TextNode("test", TextType.BOLD_TEXT)
    assert repr(node) == "TextNode(test, b, None)"


def test_repr_formats_text_node_fields_with_url() -> None:
    node = TextNode("boot.dev", TextType.ANCHOR_TEXT, "https://boot.dev")
    assert repr(node) == "TextNode(boot.dev, a, https://boot.dev)"


def test_text_node_equality_with_non_text_node_returns_false() -> None:
    node = TextNode("test", TextType.PLAIN_TEXT)
    assert (node == "test") is False


def test_text_node_reverse_equality_with_non_text_node_returns_false() -> None:
    node = TextNode("test", TextType.PLAIN_TEXT)
    assert ("test" == node) is False


# text_node_to_leaf_node conversion tests
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
