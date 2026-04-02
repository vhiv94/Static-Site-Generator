from html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        if not tag:
            raise ValueError("Error: ParentNode: parent nodes MUST have a tag")
        if not children:
            raise ValueError("Error: ParentNode: parent nodes MUST contain children")
        super().__init__(tag, None, children, props)

    @HTMLNode.value.setter
    def value(self, val: str | None) -> None:
        raise AttributeError("Error: ParentNode: value cannot be set on parent nodes")

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Error: ParentNode: parent nodes MUST have a tag")
        if not self.children:
            raise ValueError("Error: ParentNode: parent nodes MUST contain children")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
