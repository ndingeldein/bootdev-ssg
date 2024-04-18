import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown. Delimiter not closed.")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], text_type_text))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        image_matches = extract_markdown_images(text)
        if len(image_matches) == 0:
            new_nodes.append(node)
            continue
        for image in image_matches:
            parts = text.split(f"![{image[0]}]({image[1]})")
            if len(parts) != 2:
                raise ValueError("Invalid Markdown. Image not closed.")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            text = parts[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        matches = extract_markdown_links(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for link in matches:
            parts = text.split(f"[{link[0]}]({link[1]})")
            if len(parts) != 2:
                raise ValueError("Invalid Markdown. Image not closed.")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = parts[1]

        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
