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
        if delimiter not in node.text or node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        split_node: list = [(x, node.text_type if i%2==0 else text_type) for i,x in enumerate(node.text.split(delimiter))]
        if split_node[0][0] == "":
            del split_node[0]
        if split_node[-1][0] == "":
            split_node.pop()
        new_nodes.extend(list(map(lambda elem: TextNode(elem[0], elem[1]), split_node)))
 
    return new_nodes

node = TextNode("_This_ is **bold** text with a `code block` word", TextType.PLAIN_TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
new_nodes2 = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
new_nodes3 = split_nodes_delimiter(new_nodes2, "_", TextType.ITALIC_TEXT)