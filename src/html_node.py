from __future__ import annotations
from abc import ABC, abstractmethod


class HTMLNode(ABC):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if tag is not None and not isinstance(tag, str):
            raise TypeError("Error: HTMLNode: tags must be a string or None")
        if value is not None and not isinstance(value, str):
            raise TypeError("Error: HTMLNode: values must be a string or None")
        if children is not None:
            if not isinstance(children, list):
                raise TypeError(
                    "Error: HTMLNode: children must be a list of HTMLNode subclasses or None"
                )
            if not all(isinstance(child, HTMLNode) for child in children):
                raise TypeError(
                    "Error: HTMLNode: each child must be an HTMLNode subclass"
                )
        if props is not None:
            if not isinstance(props, dict):
                raise TypeError(
                    "Error: HTMLNode: props must be a dictionary of string/string pairs or None"
                )
            if not all(
                isinstance(key, str) and isinstance(val, str)
                for key, val in props.items()
            ):
                raise TypeError(
                    "Error: HTMLNode: props must be a dictionary of string/string pairs or None"
                )

        self.tag = tag
        self._value = value
        self._children = children
        self.props = props

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, val: str | None) -> None:
        self._value = val

    @property
    def children(self) -> list[HTMLNode] | None:
        return self._children

    @children.setter
    def children(self, val: list[HTMLNode] | None) -> None:
        self._children = val

    @abstractmethod
    def to_html(self) -> str:
        pass

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
