from text_node import TextNode, TextType
from html_node import HTMLNode
from leaf_node import LeafNode
from parent_node import ParentNode


def main() -> None:
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node)
    print(node.to_html())


if __name__ == "__main__":
    main()
