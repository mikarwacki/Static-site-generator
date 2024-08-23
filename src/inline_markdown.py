from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)
import re

def text_to_textnodes(text):
    delimiter_map = {
        text_type_bold: "**",
        text_type_italic: "*",
        text_type_code: "`"
    }
    nodes = [TextNode(text, text_type_text)]
    for text_type in delimiter_map:
        nodes = split_nodes_delimiter(nodes, delimiter_map[text_type], text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0 and len(sections[0]) < len(old_node.text):
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        extracted_images = extract_markdown_images(old_node.text)
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue
        text_left = old_node.text
        for image in extracted_images:
            split_text = text_left.split(f"![{image[0]}]({image[1]})", 1)
            split_nodes.append(TextNode(split_text[0], text_type_text))
            split_nodes.append(TextNode(image[0], text_type_image, image[1]))
            text_left = split_text[1]
        if len(text_left) > 0:
            split_nodes.append(TextNode(text_left, text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        text_left = old_node.text
        for link in extracted_links:
            split_text = text_left.split(f"[{link[0]}]({link[1]})", 1)
            split_nodes.append(TextNode(split_text[0], text_type_text))
            split_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text_left = split_text[1]
        if len(text_left) > 0:
            split_nodes.append(TextNode(text_left, text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes
 
def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    image_matches = re.findall(regex, text)
    return image_matches 

def extract_markdown_links(text):
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links_matches = re.findall(regex, text)
    return links_matches        
