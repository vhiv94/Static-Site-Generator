import pytest
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
    assert repr(node) == "TextNode(test, bold, None)"


def test_repr_formats_text_node_fields_with_url() -> None:
    node = TextNode("boot.dev", TextType.ANCHOR_TEXT, "https://boot.dev")
    assert repr(node) == "TextNode(boot.dev, hyperlink, https://boot.dev)"


def test_text_node_equality_with_non_text_node_returns_false() -> None:
    node = TextNode("test", TextType.PLAIN_TEXT)
    assert (node == "test") is False


def test_text_node_reverse_equality_with_non_text_node_returns_false() -> None:
    node = TextNode("test", TextType.PLAIN_TEXT)
    assert ("test" == node) is False
