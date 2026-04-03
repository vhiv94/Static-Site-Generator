import pytest

from html_node import HTMLNode
from src.md_to_html import (
    markdown_to_html,
    text_to_leaf_nodes,
    extract_links_factory,
    URL_REGEX,
    IMAGE_REGEX,
    split_nodes_on_links,
    split_nodes_on_delimiter,
    text_node_to_leaf_node,
    split_markdown_blocks,
    get_block_type_from_block,
<<<<<<< HEAD
    _list_to_list_node,
=======
    _list_to_list_nodes,
>>>>>>> 9daa415 (finish markdown to html and start on copy generate from static)
    _parse_list_nodes_r,
)
from parent_node import DivNode
from text_node import BlockType, TextNode, TextType


def assert_leaf_nodes(
    nodes: list[HTMLNode],
    expected: list[tuple[str | None, str | None, dict[str, str] | None]],
) -> None:
    assert all(isinstance(node, HTMLNode) for node in nodes)
    assert [(node.tag, node.value, node.attributes) for node in nodes] == expected


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
    node = TextNode("link text", TextType.LINK, url)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == "a"
    assert leaf_node.value == "link text"
    assert leaf_node.attributes == {"href": url}


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
    node = TextNode("link text", TextType.LINK, url)

    with pytest.raises(ValueError, match="invalid url"):
        text_node_to_leaf_node(node)


def test_text_node_to_leaf_node_anchor_requires_url() -> None:
    node = TextNode("link text", TextType.LINK)

    with pytest.raises(ValueError, match="Links need a url"):
        text_node_to_leaf_node(node)


@pytest.mark.parametrize(
    "url", ["/image.png", "./assets/image.png", "../images/photo.jpg"]
)
def test_text_node_to_leaf_node_alt_accepts_valid_path_prefixes(url: str) -> None:
    node = TextNode("hero image", TextType.IMAGE, url)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == "img"
    assert leaf_node.value is None
    assert leaf_node.attributes == {"src": url, "alt": "hero image"}


@pytest.mark.parametrize(
    "url",
    [
        "images/photo.jpg",
        "C:/images/photo.jpg",
        "ftp://cdn.example.com/image.png",
    ],
)
def test_text_node_to_leaf_node_alt_rejects_invalid_path_prefixes(url: str) -> None:
    node = TextNode("hero image", TextType.IMAGE, url)

    with pytest.raises(ValueError, match="ivalid path"):
        text_node_to_leaf_node(node)


def test_text_node_to_leaf_node_alt_requires_url() -> None:
    node = TextNode("hero image", TextType.IMAGE)

    with pytest.raises(ValueError, match="invalid path to image"):
        text_node_to_leaf_node(node)


@pytest.mark.parametrize(
    ("text_type", "expected_tag"),
    [
        (TextType.PLAIN, None),
        (TextType.BOLD, "b"),
        (TextType.ITALIC, "i"),
        (TextType.CODE, "code"),
    ],
)
def test_text_node_to_leaf_node_non_link_or_image_types_map_to_expected_leaf_tags(
    text_type: TextType, expected_tag: str | None
) -> None:
    node = TextNode("plain value", text_type)
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.tag == expected_tag
    assert leaf_node.value == "plain value"
    assert leaf_node.attributes is None


def test_text_node_to_leaf_node_anchor_allows_leading_whitespace_and_mixed_case_scheme() -> (
    None
):
    node = TextNode("link text", TextType.LINK, "   HtTpS://Boot.Dev/path")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.attributes == {"href": "   HtTpS://Boot.Dev/path"}


def test_text_node_to_leaf_node_anchor_preserves_original_href_value() -> None:
    node = TextNode("link text", TextType.LINK, "  HTTPS://Boot.Dev")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.attributes == {"href": "  HTTPS://Boot.Dev"}


def test_text_node_to_leaf_node_alt_preserves_original_src_and_alt_values() -> None:
    node = TextNode("Profile image", TextType.IMAGE, "   ../assets/pic.png")
    leaf_node = text_node_to_leaf_node(node)

    assert leaf_node.attributes == {
        "src": "   ../assets/pic.png",
        "alt": "Profile image",
    }


def test_split_nodes_delimiter_returns_original_plain_node_when_delimiter_missing() -> (
    None
):
    nodes = [TextNode("plain text only", TextType.PLAIN)]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [TextNode("plain text only", TextType.PLAIN)]


def test_split_nodes_delimiter_splits_plain_text_into_alternating_types() -> None:
    nodes = [TextNode("start **bold** end", TextType.PLAIN)]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [
        TextNode("start ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" end", TextType.PLAIN),
    ]


def test_split_nodes_delimiter_does_not_split_non_plain_nodes() -> None:
    nodes = [TextNode("**not split**", TextType.CODE)]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [TextNode("**not split**", TextType.CODE)]


def test_split_nodes_delimiter_drops_leading_empty_split_segment() -> None:
    nodes = [TextNode("**bold** tail", TextType.PLAIN)]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [
        TextNode("bold", TextType.BOLD),
        TextNode(" tail", TextType.PLAIN),
    ]


def test_split_nodes_delimiter_drops_trailing_empty_split_segment() -> None:
    nodes = [TextNode("head **bold**", TextType.PLAIN)]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [
        TextNode("head ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
    ]


def test_split_nodes_delimiter_preserves_order_in_mixed_plain_and_non_plain_nodes() -> (
    None
):
    nodes = [
        TextNode("alpha **beta**", TextType.PLAIN),
        TextNode("**leave me**", TextType.CODE),
        TextNode("gamma **delta** epsilon", TextType.PLAIN),
    ]
    result = split_nodes_on_delimiter(nodes, "**", TextType.BOLD)
    assert result == [
        TextNode("alpha ", TextType.PLAIN),
        TextNode("beta", TextType.BOLD),
        TextNode("**leave me**", TextType.CODE),
        TextNode("gamma ", TextType.PLAIN),
        TextNode("delta", TextType.BOLD),
        TextNode(" epsilon", TextType.PLAIN),
    ]


@pytest.mark.parametrize(
    "text",
    [
        "start **bold end",
        "start **bold** mid **tail",
        "**lead only",
    ],
)
def test_split_nodes_delimiter_raises_on_imbalanced_delimiters(text: str) -> None:
    nodes = [TextNode(text, TextType.PLAIN)]

    with pytest.raises(Exception, match="Invalid Markdown syntax"):
        split_nodes_on_delimiter(nodes, "**", TextType.BOLD)


def test_text_to_leaf_nodes_splits_in_current_delimiter_sequence() -> None:
    result = text_to_leaf_nodes("A `code` B **bold** C _italics_ D")

    assert_leaf_nodes(
        result,
        [
            (None, "A ", None),
            ("code", "code", None),
            (None, " B ", None),
            ("b", "bold", None),
            (None, " C ", None),
            ("i", "italics", None),
            (None, " D", None),
        ],
    )


@pytest.mark.parametrize(
    ("nodes", "is_url", "expected"),
    [
        (
            [TextNode("prefix [docs](https://boot.dev) suffix", TextType.PLAIN)],
            True,
            [
                TextNode("prefix ", TextType.PLAIN),
                TextNode("docs", TextType.LINK, "https://boot.dev"),
                TextNode(" suffix", TextType.PLAIN),
            ],
        ),
        (
            [TextNode("prefix ![hero](./hero.png) suffix", TextType.PLAIN)],
            False,
            [
                TextNode("prefix ", TextType.PLAIN),
                TextNode("hero", TextType.IMAGE, "./hero.png"),
                TextNode(" suffix", TextType.PLAIN),
            ],
        ),
        (
            [TextNode("[docs](https://boot.dev)", TextType.BOLD)],
            True,
            [TextNode("[docs](https://boot.dev)", TextType.BOLD)],
        ),
    ],
)
def test_split_nodes_on_links_respects_current_is_url_routing(
    nodes: list[TextNode], is_url: bool, expected: list[TextNode]
) -> None:
    assert split_nodes_on_links(nodes, is_url=is_url) == expected


@pytest.mark.parametrize(
    "text",
    [
        "start _italics end",
        "start `code end",
        "**bold*",
        "*italics**",
    ],
)
def test_text_to_leaf_nodes_raises_for_unmatched_delimiters(text: str) -> None:
    with pytest.raises(Exception, match="Invalid Markdown syntax"):
        text_to_leaf_nodes(text)


def test_text_to_leaf_nodes_future_supports_link_segments() -> None:
    result = text_to_leaf_nodes("before [docs](https://boot.dev) after")

    assert_leaf_nodes(
        result,
        [
            (None, "before ", None),
            ("a", "docs", {"href": "https://boot.dev"}),
            (None, " after", None),
        ],
    )


def test_text_to_leaf_nodes_future_supports_image_segments() -> None:
    result = text_to_leaf_nodes("before ![hero](./hero.png) after")

    assert_leaf_nodes(
        result,
        [
            (None, "before ", None),
            ("img", None, {"src": "./hero.png", "alt": "hero"}),
            (None, " after", None),
        ],
    )


def test_text_to_leaf_nodes_future_supports_mixed_delimiter_and_link_image() -> None:
    result = text_to_leaf_nodes(
        "A **bold** [docs](https://boot.dev) ![hero](./hero.png)"
    )

    assert_leaf_nodes(
        result,
        [
            (None, "A ", None),
            ("b", "bold", None),
            (None, " ", None),
            ("a", "docs", {"href": "https://boot.dev"}),
            (None, " ", None),
            ("img", None, {"src": "./hero.png", "alt": "hero"}),
        ],
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Read [Boot.dev Docs](https://boot.dev/docs) and "
            "[Course Outline](../course-outline.md).",
            [
                ("Boot.dev Docs", "https://boot.dev/docs"),
                ("Course Outline", "../course-outline.md"),
            ],
        ),
        (
            "Go to [week 2 notes 2026](./notes/week-2.md)",
            [("week 2 notes 2026", "./notes/week-2.md")],
        ),
        (
            "Bad [ftp link](ftp://example.com) "
            "and bad [space target](https://example.com/has space)",
            [],
        ),
    ],
)
def test_extract_links_factory_url_regex_extracts_expected_matches(
    text: str, expected: list[tuple[str, str]]
) -> None:
    extract_links = extract_links_factory(URL_REGEX)
    assert extract_links(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "![hero image](./assets/hero.png) and ![diagram 2](../images/diag-2.webp)",
            [
                ("hero image", "./assets/hero.png"),
                ("diagram 2", "../images/diag-2.webp"),
            ],
        ),
        (
            "![cdn](https://cdn.example.com/image.png)",
            [("cdn", "https://cdn.example.com/image.png")],
        ),
        ("![ftp](ftp://cdn.example.com/image.png)", []),
    ],
)
def test_extract_links_factory_image_regex_extracts_expected_matches(
    text: str, expected: list[tuple[str, str]]
) -> None:
    extract_images = extract_links_factory(IMAGE_REGEX)
    assert extract_images(text) == expected


def test_split_markdown_blocks_splits_multiple_paragraph_blocks() -> None:
    markdown = "first paragraph\n\nsecond paragraph\n\nthird paragraph"
    assert split_markdown_blocks(markdown) == [
        "first paragraph",
        "second paragraph",
        "third paragraph",
    ]


def test_split_markdown_blocks_trims_outer_whitespace_before_split() -> None:
    markdown = "\n\n  first paragraph\n\nsecond paragraph  \n\n"
    assert split_markdown_blocks(markdown) == ["first paragraph", "second paragraph"]


def test_split_markdown_blocks_keeps_single_newlines_within_block() -> None:
    markdown = "line one\nline two\nline three"
    assert split_markdown_blocks(markdown) == ["line one\nline two\nline three"]


def test_split_markdown_blocks_returns_single_block_for_single_paragraph() -> None:
    markdown = "just one block"
    assert split_markdown_blocks(markdown) == ["just one block"]


def test_split_markdown_blocks_raises_for_extra_blank_lines_between_blocks() -> None:
    markdown = "first\n\n\n\nsecond"
    with pytest.raises(ValueError, match="too much white space in markdown file"):
        split_markdown_blocks(markdown)


@pytest.mark.parametrize(
    ("block", "expected"),
    [
        ("# heading", BlockType.HEADING),
        ("```code```", BlockType.CODE),
        ("> quote", BlockType.QUOTE),
        ("- item", BlockType.UNORDERED_LIST),
        ("* item", BlockType.UNORDERED_LIST),
        ("1. first", BlockType.ORDERED_LIST),
        ("2. second", BlockType.ORDERED_LIST),
        ("10. tenth", BlockType.ORDERED_LIST),
        ("paragraph text", BlockType.PARAGRAPH),
    ],
)
def test_get_block_type_from_block_detects_types_from_first_character(
    block: str, expected: BlockType
) -> None:
    assert get_block_type_from_block(block) == expected


def test_get_block_type_from_block_requires_space_after_ordered_list_marker() -> None:
    assert get_block_type_from_block("2.second item") == BlockType.PARAGRAPH


def test_get_block_type_from_block_uses_first_character_not_following_lines() -> None:
    block = "paragraph intro\n- nested list line"
    assert get_block_type_from_block(block) == BlockType.PARAGRAPH


def test_markdown_to_html_converts_heading_paragraph_and_quote_blocks() -> None:
    markdown = "# Heading One\n\nParagraph body text\n\n> Quoted line"

    node = markdown_to_html(markdown)

    assert isinstance(node, DivNode)
    assert node.to_html() == (
        "<div><h1>Heading One</h1><p>Paragraph body text</p>"
        "<blockquote>Quoted line</blockquote></div>"
    )


def test_markdown_to_html_converts_code_block_without_language_and_preserves_newlines() -> (
    None
):
    markdown = "```\nline 1\nline 2\n```"

    node = markdown_to_html(markdown)

    assert isinstance(node, DivNode)
    assert node.to_html() == "<div><pre><code>\nline 1\nline 2\n</code></pre></div>"


def test_markdown_to_html_converts_code_block_with_language_class_attribute() -> None:
    markdown = "```python\nprint('hello')\n```"

    node = markdown_to_html(markdown)

    assert isinstance(node, DivNode)
    assert (
        node.to_html()
        == "<div><pre><code class=\"language-python\">\nprint('hello')\n</code></pre></div>"
    )


@pytest.mark.parametrize(
    ("markdown", "expected_html"),
    [
        (
            "- first\n- second",
            "<div><ul><li>first</li><li>second</li></ul></div>",
        ),
        (
            "1. first\n2. second",
            "<div><ol><li>first</li><li>second</li></ol></div>",
        ),
    ],
)
def test_markdown_to_html_converts_basic_list_blocks(
    markdown: str, expected_html: str
) -> None:
    node = markdown_to_html(markdown)

    assert isinstance(node, DivNode)
    assert node.to_html() == expected_html


def test_markdown_to_html_converts_tab_indented_nested_unordered_list() -> None:
    markdown = "- parent\n\t- child one\n\t- child two\n- sibling"

    node = markdown_to_html(markdown)

    assert isinstance(node, DivNode)
    assert (
        node.to_html()
        == "<div><ul><li>parent<ul><li>child one</li><li>child two</li></ul></li>"
        "<li>sibling</li></ul></div>"
    )


@pytest.mark.parametrize(
    ("lines", "is_ordered", "expected"),
    [
        (
            ["- alpha", "- beta"],
            False,
            [("li", "alpha"), ("li", "beta")],
        ),
        (
            ["1. alpha", "2. beta"],
            True,
            [("li", "alpha"), ("li", "beta")],
        ),
    ],
)
def test_parse_list_nodes_builds_li_nodes_for_ordered_and_unordered_lists(
    lines: list[str], is_ordered: bool, expected: list[tuple[str, str]]
) -> None:
<<<<<<< HEAD
    nodes = _list_to_list_node(lines, is_ordered=is_ordered)
=======
    nodes = _list_to_list_nodes(lines, is_ordered=is_ordered)
>>>>>>> 9daa415 (finish markdown to html and start on copy generate from static)

    assert [(node.tag, node.children[0].value) for node in nodes] == expected


def test_parse_list_level_handles_indent_increase_then_decrease() -> None:
    lines = ["- parent", "\t- child", "- sibling"]

    nodes, idx = _parse_list_nodes_r(lines, idx=0, depth=0, is_ordered=False)

    assert idx == 3
    assert len(nodes) == 2
    assert nodes[0].tag == "li"
    assert nodes[0].children[0].value == "parent"
    assert nodes[0].children[1].tag == "ul"
    assert nodes[0].children[1].children[0].children[0].value == "child"
    assert nodes[1].children[0].value == "sibling"


@pytest.mark.parametrize(
    ("lines", "error"),
    [
        (["\t- orphan child"], "nested list without parent item"),
        (["- valid", "invalid marker line"], "line isn't formatted properly"),
    ],
)
def test_parse_list_helpers_raise_errors_for_malformed_input(
    lines: list[str], error: str
) -> None:
    with pytest.raises(ValueError, match=error):
<<<<<<< HEAD
        _list_to_list_node(lines, is_ordered=False)
=======
        _list_to_list_nodes(lines, is_ordered=False)
>>>>>>> 9daa415 (finish markdown to html and start on copy generate from static)
