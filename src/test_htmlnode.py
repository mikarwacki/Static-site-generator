import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_string(self):
        node = HTMLNode("tag", "value", [], {})
        string_repr = "HTMLNode(tag, value, children: [], {})"
        self.assertEqual(repr(node), string_repr)

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", [], {
        "href": "https://www.google.com", 
        "target": "_blank",
        })
        props = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), props)

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_node = '<p>This is a paragraph of text.</p>'
        html_node2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), html_node)
        self.assertEqual(node2.to_html(), html_node2)

    def test_parent_node_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        html_node = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), html_node)

if __name__ == "__main__":
    unittest.main()
