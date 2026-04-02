import pytest
from leaf_node import LeafNode


def test_leaf_node_stores_tag_value() -> None:
    node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
    assert node.tag == "a"


def test_leaf_node_stores_value_value() -> None:
    node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
    assert node.value == "boot.dev"


def test_leaf_node_stores_props_value() -> None:
    node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
    assert node.props == {"href": "https://boot.dev"}


def test_leaf_node_sets_children_to_none() -> None:
    node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
    assert node.children is None


def test_leaf_node_raises_when_children_are_set() -> None:
    node = LeafNode("p", "hello")
    with pytest.raises(AttributeError):
        node.children = []


def test_leaf_node_allows_none_value_for_void_element_style_render() -> None:
    node = LeafNode("img", None, {"href": "blah"})  # type: ignore[arg-type]
    assert node.to_html() == '<img href="blah" />'


@pytest.mark.parametrize("tag", [None, ""])
def test_to_html_returns_raw_value_when_tag_is_falsy(tag: str | None) -> None:
    node = LeafNode(tag, "raw text", {"class": "ignored"})  # type: ignore[arg-type]
    assert node.to_html() == "raw text"


@pytest.mark.parametrize(
    "tag, value, props, expected",
    [
        ("p", "hello", None, "<p>hello</p>"),
        (
            "a",
            "boot.dev",
            {"href": "https://boot.dev"},
            '<a href="https://boot.dev">boot.dev</a>',
        ),
        (
            "custom-element",
            "value",
            {"data-id": "42", "aria-label": "item"},
            '<custom-element data-id="42" aria-label="item">value</custom-element>',
        ),
    ],
)
def test_to_html_returns_wrapped_html_for_tagged_leaf_nodes(
    tag: str,
    value: str,
    props: dict[str, str] | None,
    expected: str,
) -> None:
    node = LeafNode(tag, value, props)
    assert node.to_html() == expected


def test_to_html_returns_self_closing_tag_when_value_becomes_none_after_init() -> None:
    node = LeafNode("p", "hello")
    node.value = None
    assert node.to_html() == "<p />"


def test_to_html_allows_empty_string_value() -> None:
    node = LeafNode("p", "")
    assert node.to_html() == "<p></p>"


def test_repr_returns_leaf_node_with_none_props() -> None:
    node = LeafNode("p", "hello")
    assert repr(node) == "LeafNode(p, hello, None)"


def test_repr_returns_leaf_node_with_populated_props() -> None:
    node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
    assert repr(node) == "LeafNode(a, boot.dev, {'href': 'https://boot.dev'})"
