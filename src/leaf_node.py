from html_node import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    @HTMLNode.children.setter
    def children(self, val: list[HTMLNode] | None) -> None:
        raise AttributeError("Error: LeafNode: children cannot be set on leaf nodes")

    def to_html(self) -> str:
        if not self.tag:
            return "" if self.value is None else self.value
        elif self.value is None:
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
