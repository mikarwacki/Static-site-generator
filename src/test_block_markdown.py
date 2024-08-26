import unittest

from block_markdown import (
    markdown_to_blokcs,
    block_to_block,
    markdown_to_html
)

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
        expected_html = ["<blockquote>some new quote</blockquote>"]
        html = markdown_to_html(markdown)
        self.assertEqual(html, expected_html)
    
    def test_markdown_code(self):
        markdown = '''```some new code in here```'''
        expected_html = ["<pre><code>some new code in here</code></pre>"]
        html = markdown_to_html(markdown)
        self.assertEqual(html, expected_html)
    
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
        expected_html = ["<h1>this is the heading one</h1>", 
                     "<h2>this is another heading</h2>", 
                     "<p>here <b>starts bold</b> the paragaph\n</p>", 
                     "<blockquote>here goes the <i>italic</i> quote</blockquote>",
                     "<pre><code>some code</code></pre>",
                     "<ul><li>random list</li><li>item</li><li>item</li></ul>",
                     "<ol><li>ordered list</li><li>item</li></ol>"]
        html = markdown_to_html(markdown)
        self.assertEqual(html, expected_html)



if __name__ == "__main__":
    unittest.main()