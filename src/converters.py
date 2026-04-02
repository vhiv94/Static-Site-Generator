from text_node import TextNode, TextType
# from parent_node import ParentNode
from leaf_node import LeafNode


def text_node_to_leaf_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.ANCHOR_TEXT:
        if text_node.url is None:
            raise ValueError("Error: text node to leaf node: Links need a url")
        url = text_node.url.lstrip().lower()
        if url.startswith(("http://", "https://", "/", "./", "../", "#", "mailto:")):
            return LeafNode(text_node.text_type.value, text_node.text, {"href": text_node.url})
        else:
            raise ValueError("Error: text node to leaf node: invalid url")
    
    if text_node.text_type == TextType.ALT_TEXT:
        if text_node.url is None:
            raise ValueError("Error: text node to leaf node: Images need a url")
        url = text_node.url.lstrip()
        if url.startswith(("/", "./", "../")):
            return LeafNode(text_node.text_type.value, None, {"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError("Error: text node to leaf node: invalid path to image")
        
    return LeafNode(text_node.text_type.value, text_node.text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            part_type = TextType.PLAIN_TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, part_type))
 
    return new_nodes