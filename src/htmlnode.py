class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        res = []
        for key, val in self.props.items():
            res.append(f'{key}="{val}"')
        return " " + " ".join(res)

    def text_node_to_html_node(self, text_node):
        match text_node.text_type:
            case "text":
                return LeafNode(None, text_node.text)
            case "bold":
                return LeafNode("b", text_node.text)
            case "italic":
                return LeafNode("i", text_node.text)
            case "code":
                return LeafNode("code", text_node.text)
            case "link":
                return LeafNode("a", text_node.text, {"href":text_node.url})
            case "img":
                return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Invalid text type")

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return self.enclose_value()

    def enclose_value(self):
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("The node has to have a tag")
        if self.children == None and type(self) != "__main__.LeafNode":
            raise ValueError("Parent node has to have at least one child")
        if len(self.children) == 0:
            return self.to_html()
        res = ""
        for child in self.children:
            res += child.to_html()
        return f"<{self.tag}>{res}</{self.tag}>"

