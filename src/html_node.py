from __future__ import annotations
from functools import reduce


class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str| None = None, 
            children: list[HTMLNode] | None = None, 
            props: dict[str, str] | None = None
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return reduce(lambda acc, item: acc + f' {item[0]}="{item[1]}"', self.props.items(), "")
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"