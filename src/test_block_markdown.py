import unittest

from block_markdown import (
    markdown_to_blokcs,
    block_to_block,
    markdown_to_html_node,
)
from markdown_to_html import extract_title

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = '''# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item''' 

        expected_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        blocks = markdown_to_blokcs(markdown)
        self.assertEqual(blocks, expected_blocks)
    
    def test_markdown_to_blocks_empty(self):
        markdown = ""
        expected_blocks = ['']
        blocks = markdown_to_blokcs(markdown)
        self.assertEqual(blocks, expected_blocks)

    def test_block_to_block_paragraph(self):
        block = "Some new text"
        expected = "paragraph"
        result = block_to_block(block)
        self.assertEqual(result, expected)

    def test_block_to_block_heading(self):
        block = "Some new text"
        expected = "paragraph"
        result = block_to_block(block)
        self.assertEqual(result, expected)

    def test_block_to_block_code(self):
        block = "```Some new text ```"
        expected = "code"
        result = block_to_block(block)
        self.assertEqual(result, expected)

    def test_block_to_block_quote(self):
        block = ">Some new text"
        expected = "quote"
        result = block_to_block(block)
        self.assertEqual(result, expected)

    def test_block_to_block_unordered_list(self):
        block = "* Some new text"
        dash_block = "- Some new text"
        expected = "unordered_list"
        result = block_to_block(block)
        self.assertEqual(result, expected)
        result = block_to_block(dash_block)
        self.assertEqual(result, expected)

    def test_block_to_block_ordered_list(self):
        block = "1. Some new text"
        expected = "ordered_list"
        result = block_to_block(block)
        self.assertEqual(result, expected)       

class TestMarkdownToHtml(unittest.TestCase):

    def test_markdown_paragraph(self):
        markdown = '''> some new quote '''
        expected_html = "<div><blockquote>some new quote</blockquote></div>"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.to_html(), expected_html)
    
    def test_markdown_code(self):
        markdown = '''```some new code in here```'''
        expected_html = "<div><pre><code>some new code in here</code></pre></div>"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.to_html(), expected_html)
    
    def test_full_markdown_file(self):
        markdown = '''
        # this is the heading one
        ## this is another heading

        here **starts bold** the paragaph

        > here goes the *italic* quote

        ```some code```

        * random list
        - item
        * item

        1. ordered list
        2. item
        '''
        expected_html = "<div><h1>this is the heading one</h1><h2>this is another heading</h2><p>here <b>starts bold</b> the paragaph</p><blockquote>here goes the <i>italic</i> quote</blockquote><pre><code>some code</code></pre><ul><li>random list</li><li>item</li><li>item</li></ul><ol><li>ordered list</li><li>item</li></ol></div>"
        html = markdown_to_html_node(markdown)
        self.assertEqual(html.to_html(), expected_html)


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# header"
        expected = "header"
        result = extract_title(markdown) 
        self.assertEqual(result, expected)

    def test_no_title(self):
        markdown = "no header"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()