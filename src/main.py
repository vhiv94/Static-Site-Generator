from textnode import TextNode, TextType


def main() -> None:
    test_node = TextNode("This is some anchor text", TextType.ANCHOR_TEXT, "https://www.boot.dev")
    print(test_node)

if __name__ == "__main__":
    main()