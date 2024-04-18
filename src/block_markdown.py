from parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

from htmlnode import HTMLNode
from parentnode import ParentNode

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n\n"):
        line = line.strip()
        if line == "":
            continue
        blocks.append(line)
    return blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if is_heading(markdown):
        return block_type_heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return block_type_code
    if markdown.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return block_type_paragraph
        return block_type_quote
    if markdown.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    if markdown.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                return block_type_paragraph
        return block_type_ordered_list
    return block_type_paragraph


def is_heading(markdown):
    # starts with #, ##, ###, ####, #####, ###### followed by a space
    return (
        markdown.startswith("#") and markdown[1] == " "
        or markdown.startswith("##") and markdown[2] == " "
        or markdown.startswith("###") and markdown[3] == " "
        or markdown.startswith("####") and markdown[4] == " "
        or markdown.startswith("#####") and markdown[5] == " "
        or markdown.startswith("######") and markdown[6] == " "
    )

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_html_node(block)
        nodes.append(node)
    return ParentNode("div", nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_block_to_html_node(block)
    if block_type == block_type_heading:
        return heading_block_to_html_node(block)
    if block_type == block_type_code:
        return code_block_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_block_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_block_to_html_node(block)
    if block_type == block_type_quote:
        return quote_block_to_html_node(block)
    raise ValueError("Unknown block type")

def text_to_child_nodes(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append(text_node_to_html_node(text_node))

    return child_nodes

def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    p = " ".join(lines)
    child_nodes = text_to_child_nodes(p)
    return ParentNode("p", child_nodes)

def heading_block_to_html_node(block):
    level = 1
    while block[level] == "#":
        level += 1
    if block[level] != " ":
        raise ValueError("Invalid heading")
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level+1:]
    child_nodes = text_to_child_nodes(text)

    return ParentNode(f"h{level}", child_nodes)

def code_block_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    child_nodes = text_to_child_nodes(text)

    code_node = ParentNode("code", child_nodes)
    return ParentNode("pre", [code_node])

def quote_block_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Invalid quote block")
        stripped_lines.append(line[2:])
    child_nodes = text_to_child_nodes(" ".join(stripped_lines))
    return ParentNode("blockquote", child_nodes)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if not line.startswith("* "):
            raise ValueError("Invalid unordered list block")
        child_nodes = text_to_child_nodes(line[2:])
        list_items.append(ParentNode("li", child_nodes))

    return ParentNode("ul", list_items)


def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            raise ValueError(f"Invalid ordered list block:{i}")
        child_nodes = text_to_child_nodes(line[3:])
        list_items.append(ParentNode("li", child_nodes))

    return ParentNode("ol", list_items)
