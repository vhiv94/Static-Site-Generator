import pytest
from leaf_node import LeafNode
from parent_node import ParentNode


@pytest.mark.parametrize("tag", [None, ""])
def test_parent_node_init_raises_when_tag_is_falsy(tag: str | None) -> None:
    with pytest.raises(ValueError):
        ParentNode(tag, [LeafNode("span", "child")])  # type: ignore[arg-type]


@pytest.mark.parametrize("children", [None, []])
def test_parent_node_init_raises_when_children_missing(
    children: list[LeafNode] | None,
) -> None:
    with pytest.raises(ValueError):
        ParentNode("div", children)  # type: ignore[arg-type]


def test_parent_node_to_html_renders_direct_children() -> None:
    node = ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " plain")])
    assert node.to_html() == "<p><b>Bold</b> plain</p>"


def test_parent_node_to_html_renders_nested_children() -> None:
    nested = ParentNode("li", [LeafNode(None, "second item")])
    node = ParentNode("ul", [LeafNode("li", "first item"), nested])
    assert node.to_html() == "<ul><li>first item</li><li>second item</li></ul>"


def test_parent_node_to_html_includes_props() -> None:
    node = ParentNode("div", [LeafNode(None, "content")], {"class": "container"})
    assert node.to_html() == '<div class="container">content</div>'


def test_parent_node_to_html_raises_when_tag_is_invalid_after_init() -> None:
    node = ParentNode("div", [LeafNode(None, "content")])
    node.tag = None
    with pytest.raises(ValueError):
        node.to_html()


def test_parent_node_to_html_raises_when_children_invalid_after_init() -> None:
    node = ParentNode("div", [LeafNode(None, "content")])
    node.children = []
    with pytest.raises(ValueError):
        node.to_html()


def test_parent_node_raises_when_value_is_set() -> None:
    node = ParentNode("div", [LeafNode(None, "content")])
    with pytest.raises(AttributeError):
        node.value = "new value"


def test_parent_node_repr_formats_fields() -> None:
    child = LeafNode("span", "child", {"class": "x"})
    node = ParentNode("div", [child], {"id": "root"})
    assert (
        repr(node)
        == "ParentNode(div, [LeafNode(span, child, {'class': 'x'})], {'id': 'root'})"
    )
