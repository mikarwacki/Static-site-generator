import unittest

from block_markdown import (
    markdown_to_blokcs,
    block_to_block
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

if __name__ == "__main__":
    unittest.main()