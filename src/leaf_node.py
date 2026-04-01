from html_node import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, 
        tag: str, 
        value: str, 
        props: str | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props}>{self.value}</{self.tag}>"