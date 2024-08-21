import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_text_type_noteq(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "italic", None)
        self.assertNotEqual(node, node2)

    def test_url_diff(self):
        node = TextNode("This is a text node", "bold", "someUrl")
        node2 = TextNode("This is a text node", "bold", "otherUrl")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
