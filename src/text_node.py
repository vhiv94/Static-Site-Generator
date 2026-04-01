from __future__ import annotations
from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code snippet"
    ANCHOR_TEXT = "hyperlink"
    ALT_TEXT = "image link"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        return self.text == other.text\
        and self.text_type == other.text_type\
        and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"