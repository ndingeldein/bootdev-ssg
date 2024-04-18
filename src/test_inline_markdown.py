import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_links,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        code_node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([code_node], "`", text_type_code)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ])

        italic_node = TextNode("This is text with an *italicized* word", text_type_text)
        new_nodes = split_nodes_delimiter([italic_node], "*", text_type_italic)

        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", text_type_text),
            TextNode("italicized", text_type_italic),
            TextNode(" word", text_type_text),
        ])

        bold_node = TextNode("This is text with a **bolded** word", text_type_text)
        bold_node2 = TextNode("This is text without a bolded word", text_type_text)
        bold_node3 = TextNode("This is text also has a **bolded** word", text_type_text)
        bold_node4 = TextNode("This is **text** with multiple **bolded** words", text_type_text)
        new_nodes = split_nodes_delimiter([bold_node, bold_node2, bold_node3, bold_node4], "**", text_type_bold)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" word", text_type_text),
            TextNode("This is text without a bolded word", text_type_text),
            TextNode("This is text also has a ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" word", text_type_text),
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with multiple ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode(" words", text_type_text),
        ])

        # text_node = TextNode("This is text without any markdown blocks", text_type_text)
        # new_nodes = split_nodes_delimiter([text_node, boldNo], "", text_type_text)

    def test_extract_markdown_images(self):
        text = "Some text! ![image1](https://example.com/image1.png) that has images ![image2](https://example.com/image2.png) and other text"
        self.assertEqual(extract_markdown_images(text), [
            ("image1", "https://example.com/image1.png"),
            ("image2", "https://example.com/image2.png"),
        ])

    def test_extract_markdown_links(self):
        text = "Some text [link1](https://example.com/) that has links [link2](https://example.com/about) and other text"
        self.assertEqual(extract_markdown_links(text), [
            ("link1", "https://example.com/"),
            ("link2", "https://example.com/about"),
        ])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://cdn.com/image1.png) and another ![second image](https://cdn.com/image2.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual([
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://cdn.com/image1.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://cdn.com/image2.png"),
        ], new_nodes)

    def test_text_totextnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://cdn.com/image1.png) and a [link](https://boot.dev) at the end."
        nodes = text_to_textnodes(text)

        self.assertEqual(nodes, [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://cdn.com/image1.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" at the end.", text_type_text),
        ])
