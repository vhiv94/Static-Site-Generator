from ..text_node import TextNode, TextType


def test_text_nodes_with_same_fields_are_equal():
    node1 = TextNode("test", TextType.PLAIN_TEXT)
    node2 = TextNode("test", TextType.PLAIN_TEXT)
    assert node1 == node2


def test_text_nodes_with_same_url_are_equal():
    node1 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    assert node1 == node2


def test_text_nodes_with_different_text_types_are_not_equal():
    node1 = TextNode("test", TextType.PLAIN_TEXT)
    node2 = TextNode("test", TextType.BOLD_TEXT)
    assert node1 != node2


def test_text_nodes_with_different_text_are_not_equal():
    node1 = TextNode("test", TextType.PLAIN_TEXT)
    node2 = TextNode("oops", TextType.PLAIN_TEXT)
    assert node1 != node2


def test_text_nodes_with_different_urls_are_not_equal():
    node1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.ANCHOR_TEXT, "https//:test.com")
    assert node1 != node2


def test_text_nodes_with_url_and_none_url_are_not_equal():
    node1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    node2 = TextNode("test", TextType.ANCHOR_TEXT)
    assert node1 != node2


def test_text_nodes_with_empty_text_are_equal():
    node1 = TextNode("", TextType.PLAIN_TEXT)
    node2 = TextNode("", TextType.PLAIN_TEXT)
    assert node1 == node2


def test_repr_formats_text_node_fields():
    node = TextNode("test", TextType.BOLD_TEXT)
    assert repr(node) == "TextNode(test, bold, None)"