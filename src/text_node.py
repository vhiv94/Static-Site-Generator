from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = None
    BOLD_TEXT = "b"
    ITALIC_TEXT = "i"
    CODE_TEXT = "code"
    ANCHOR_TEXT = "a"
    ALT_TEXT = "img"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
