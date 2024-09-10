import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, text_type_text
from inline_markdown import(
    text_to_textnodes
)
heading = r"#{1,6}\s.*?"
code = "```"
quote = ">"
unordered_list = r"[*-]\s.*?"
ordered_list = r"[1-9]\.\s.*?"


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"
block_type_to_tag = {
    block_type_quote: "blockquote",
    block_type_ulist: "ul",
    block_type_olist: "ol",
    block_type_code: "code",
    block_type_heading: "h",
    block_type_paragraph: "p"
}

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        print(line)
        if line[0] == '#':
            return line[2:]
    raise Exception("there is no header")

def markdown_to_blokcs(markdown):
    blocks = markdown.split("\n")
    non_empty_blocks = []
    temp_blocks = []
    for block in blocks:
        if len(block.strip()) > 0:
            temp_blocks.append(block.strip())
        else:
            non_empty_blocks.append("\n".join(temp_blocks))
            temp_blocks = []
    if len(temp_blocks) > 0:
        non_empty_blocks.append("\n".join(temp_blocks))
    return non_empty_blocks

def block_to_block(block):
    is_heading = re.match(heading, block)
    if is_heading:
        return block_type_heading
    
    is_code = block[:3] == code and block[len(block) - 3:] == code
    if is_code:
        return block_type_code

    if block[:1] == quote:
        return block_type_quote

    is_unordered_list = re.match(unordered_list, block)
    if is_unordered_list:
        return block_type_ulist

    is_ordered_list = re.match(ordered_list, block)
    if is_ordered_list:
        return block_type_olist
    return block_type_paragraph
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blokcs(markdown)
    parents = []
    for block in blocks:
        parent = create_parent_node(block)
        if block_to_block(block) == block_type_heading:
            parents.extend(parent)
        elif len(parent.children) > 0:
            parents.append(parent)
    return ParentNode("div", parents)   

def create_parent_node(block):
    block_type = block_to_block(block)
    if block_type == block_type_paragraph:
        return create_paragraph(block)
    if block_type == block_type_olist:
        return create_olist(block)
    if block_type == block_type_ulist:
        return create_ulist(block)
    if block_type == block_type_code:
        return create_code(block)
    if block_type == block_type_heading:
        return create_heading(block)
    if block_type == block_type_quote:
        return create_quote(block)

def create_paragraph(block):
    nodes = []
    lines = block.split("\n")
    text = " ".join(lines)
    nodes.extend(text_to_textnodes(text))
    nodes = list(map(lambda textnode: text_node_to_html_node(textnode), nodes))
    return ParentNode("p", nodes)

def create_olist(block):
    nodes = []
    lines = block.split("\n")
    for line in lines:
        line = re.split(ordered_list, line, 1)[1]
        text_nodes = text_to_textnodes(line)
        html_nodes = []
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))
        nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", nodes)


def create_ulist(block):
    nodes = []
    lines = block.split("\n")
    for line in lines:
        line = re.split(unordered_list, line, 1)[1]
        text_nodes = text_to_textnodes(line)
        html_nodes = []
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))
        nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", nodes)

def create_code(block):
    nodes = []
    block = block[3:len(block) - 3]
    lines = block.split("\n")
    for line in lines:
        nodes.extend(text_to_textnodes(line))
    nodes = list(map(lambda textnode: text_node_to_html_node(textnode), nodes))
    return ParentNode("pre", [ParentNode("code", nodes)])

def create_quote(block):
    nodes = []
    block = block.lstrip("> ")
    lines = block.split("\n")
    for line in lines:
        line = line.lstrip(">")
        nodes.extend(text_to_textnodes(line))
    nodes = list(map(lambda textnode: text_node_to_html_node(textnode), nodes))
    return ParentNode("blockquote", nodes)

def create_heading(block):
    nodes = []
    split = block.split("\n")
    for line in split:
        count = count_hashes(line)
        line = line.lstrip("# ")
        text_nodes = text_to_textnodes(line)
        html_nodes = []
        for text_node in text_nodes:
            html_nodes.append(text_node_to_html_node(text_node))
        nodes.append(ParentNode(f"h{count}", html_nodes))
    return nodes

def count_hashes(line):
    count = 0
    for char in line:
        if char == "#":
            count += 1
    return count
