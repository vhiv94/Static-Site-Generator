import pytest
from ..html_node import HTMLNode


@pytest.mark.parametrize(
    "props, expected",
    [
        (None, ""),
        ({}, ""),
        ({"href": "https://www.google.com"}, ' href="https://www.google.com"'),
        (
            {"href": "https://www.google.com", "target": "_blank"},
            ' href="https://www.google.com" target="_blank"',
        ),
    ],
)
def test_props_to_html_formats_props(props, expected):
    test1 = HTMLNode(props=props)
    assert test1.props_to_html() == expected


def test_html_node_stores_tag_value():
    child = HTMLNode("span", "child")
    test1 = HTMLNode(
        tag="a",
        value="anchor",
        children=[child],
        props={"href": "https://www.google.com"},
    )
    assert test1.tag == "a"


def test_html_node_stores_value_value():
    child = HTMLNode("span", "child")
    test1 = HTMLNode(
        tag="a",
        value="anchor",
        children=[child],
        props={"href": "https://www.google.com"},
    )
    assert test1.value == "anchor"


def test_html_node_stores_children_value():
    child = HTMLNode("span", "child")
    test1 = HTMLNode(
        tag="a",
        value="anchor",
        children=[child],
        props={"href": "https://www.google.com"},
    )
    assert test1.children == [child]


def test_html_node_stores_props_value():
    child = HTMLNode("span", "child")
    test1 = HTMLNode(
        tag="a",
        value="anchor",
        children=[child],
        props={"href": "https://www.google.com"},
    )
    assert test1.props == {"href": "https://www.google.com"}


def test_to_html_raises_not_implemented_error():
    test1 = HTMLNode("p", "text")
    with pytest.raises(NotImplementedError):
        test1.to_html()