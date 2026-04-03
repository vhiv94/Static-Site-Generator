import pytest
from html_node import HTMLNode


class ConcreteHTMLNode(HTMLNode):
    def to_html(self) -> str:
        return ""


@pytest.mark.parametrize(
    "props, expected",
    [
        (None, ""),
        ({}, ""),
        ({"href": "https://www.google.com"}, ' href="https://www.google.com"'),
        ({"disabled": ""}, ' disabled=""'),
        (
            {"href": "https://www.google.com", "target": "_blank"},
            ' href="https://www.google.com" target="_blank"',
        ),
    ],
)
def test_props_to_html_formats_props(props, expected):
    test1 = ConcreteHTMLNode(attributes=props)
    assert test1.attributes_to_html() == expected


def test_html_node_stores_tag_value():
    node = ConcreteHTMLNode(tag="a")
    assert node.tag == "a"


def test_html_node_stores_value_value():
    node = ConcreteHTMLNode(value="anchor")
    assert node.value == "anchor"


def test_html_node_stores_children_value():
    child = ConcreteHTMLNode("span", "child")
    node = ConcreteHTMLNode(children=[child])
    assert node.children == [child]


def test_html_node_stores_props_value():
    node = ConcreteHTMLNode(attributes={"href": "https://www.google.com"})
    assert node.attributes == {"href": "https://www.google.com"}


def test_html_node_is_abstract_and_requires_to_html() -> None:
    assert "to_html" in HTMLNode.__abstractmethods__


def test_repr_returns_default_field_values():
    node = ConcreteHTMLNode()
    assert repr(node) == "HTMLNode(None, None, None, None)"


def test_repr_returns_populated_field_values():
    node = ConcreteHTMLNode(
        tag="div",
        value="hello",
        children=[],
        attributes={"class": "title"},
    )
    assert repr(node) == "HTMLNode(div, hello, [], {'class': 'title'})"


@pytest.mark.parametrize("tag", [123, 1.25, object()])
def test_html_node_init_raises_type_error_when_tag_invalid(tag: object) -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(tag=tag)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [123, 1.25, object()])
def test_html_node_init_raises_type_error_when_value_invalid(value: object) -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(value=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("children", ["child", {"a": 1}, object()])
def test_html_node_init_raises_type_error_when_children_not_list(
    children: object,
) -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(children=children)  # type: ignore[arg-type]


def test_html_node_init_raises_type_error_when_children_items_invalid() -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(children=["not-a-node"])  # type: ignore[list-item]


@pytest.mark.parametrize("props", ["props", [("k", "v")], object()])
def test_html_node_init_raises_type_error_when_props_not_dict(props: object) -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(attributes=props)  # type: ignore[arg-type]


def test_html_node_init_raises_type_error_when_props_items_invalid() -> None:
    with pytest.raises(TypeError):
        ConcreteHTMLNode(attributes={"href": 123})  # type: ignore[dict-item]
