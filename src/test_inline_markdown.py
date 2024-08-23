import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
   
    def test_bold_text(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_text(self):
        node = TextNode("This is text with a **code block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        extracted = extract_markdown_links(text)
        self.assertEqual(extracted, expected_result)

    def test_extract_markdown_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        extraced = extract_markdown_images(text)
        self.assertEqual(extraced, expected_result)

    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
        )
        expected_nodes = [
        TextNode("This is text with a link ", text_type_text),
        TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
        TextNode(" and ", text_type_text),
        TextNode("to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"),
        ]
        splited_nodes = split_nodes_image([node])
        self.assertEqual(splited_nodes, expected_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
        )
        expected_nodes = [
        TextNode("This is text with a link ", text_type_text),
        TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
        TextNode(" and ", text_type_text),
        TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
        ]
        splited_nodes = split_nodes_link([node])
        self.assertEqual(splited_nodes, expected_nodes)

    def test_split_nodes_with_normal_textnode(self):
        node = TextNode("This is textnode without any link and images", text_type_text)
        expected_nodes = [TextNode("This is textnode without any link and images", text_type_text)]
        splited_nodes = split_nodes_link([node])
        self.assertEqual(splited_nodes, expected_nodes)
        splited_nodes = split_nodes_image([node])
        self.assertEqual(splited_nodes, expected_nodes)

    def test_split_nodes_not_text_textnode(self):
        node = TextNode("This is bold text textnode", text_type_bold)
        expected_nodes = [TextNode("This is bold text textnode", text_type_bold)]
        splited_nodes = split_nodes_link([node])
        self.assertEqual(splited_nodes, expected_nodes)
        splited_nodes = split_nodes_image([node])
        self.assertEqual(splited_nodes, expected_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
        TextNode("This is ", text_type_text),
        TextNode("text", text_type_bold),
        TextNode(" with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word and a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", text_type_text),
        TextNode("link", text_type_link, "https://boot.dev"),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_text_to_textnodes_plain(self):
        text = "This is plain text without any formatting"
        excepted = [TextNode("This is plain text without any formatting", text_type_text)]
        result = text_to_textnodes(text)
        self.assertEqual(result, excepted)


if __name__ == "__main__":
    unittest.main()
