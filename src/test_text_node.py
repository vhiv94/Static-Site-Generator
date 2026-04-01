from text_node import TextNode, TextType


def test_eq():
    test1 = TextNode("test", TextType.PLAIN_TEXT)
    test2 = TextNode("test", TextType.PLAIN_TEXT)
    assert test1 == test2

def test_eq_with_url():
    test1 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    test2 = TextNode("test", TextType.PLAIN_TEXT, "http//:test.com")
    assert test1 == test2

def test_not_eq_dif_type():
    test1 = TextNode("test", TextType.PLAIN_TEXT)
    test2 = TextNode("test", TextType.BOLD_TEXT)
    assert test1 != test2

def test_not_eq_dif_text():
    test1 = TextNode("test", TextType.PLAIN_TEXT)
    test2 = TextNode("oops", TextType.PLAIN_TEXT)
    assert test1 != test2

def test_not_eq_dif_url():
    test1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    test2 = TextNode("test", TextType.ANCHOR_TEXT, "https//:test.com")
    assert test1 != test2

def test_not_eq_dif_url_none():
    test1 = TextNode("test", TextType.ANCHOR_TEXT, "http//:test.com")
    test2 = TextNode("test", TextType.ANCHOR_TEXT)
    assert test1 != test2