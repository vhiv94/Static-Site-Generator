from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Mapping


class HTMLNode(ABC):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        attributes: Mapping[str, str | int] | None = None,
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
        if attributes is not None:
            if not isinstance(attributes, dict):
                raise TypeError(
                    "Error: HTMLNode: props must be a dictionary of string/string pairs or None"
                )
            if not all(
                isinstance(key, str) and (isinstance(val, str) or isinstance(val, int))
                for key, val in attributes.items()
            ):
                raise TypeError(
                    "Error: HTMLNode: props must be a dictionary of string/string or string/int pairs or None"
                )

        self._tag = tag
        self._value = value
        self._children = children
        self.attributes = attributes

    @property
    def tag(self) -> str | None:
        return self._tag

    @tag.setter
    def tag(self, val: str | None) -> None:
        raise AttributeError("Error: HTMLNode: cannot change the tag of any node")

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

    def attributes_to_html(self) -> str:
        if self.attributes is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.attributes.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.attributes})"
