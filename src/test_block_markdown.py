import unittest

from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

   This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line



 * This is a list
* with items
"""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_block_to_block_type_headings(self):
        h1 = "# This is a heading"
        h2 = "## This is a heading"
        h3 = "### This is a heading"
        h4 = "#### This is a heading"
        h5 = "##### This is a heading"
        h6 = "###### This is a heading"
        not_heading = "#This is not a heading"
        not_heading2 = "####### This is not a heading"

        self.assertEqual(block_to_block_type(h1), block_type_heading)
        self.assertEqual(block_to_block_type(h2), block_type_heading)
        self.assertEqual(block_to_block_type(h3), block_type_heading)
        self.assertEqual(block_to_block_type(h4), block_type_heading)
        self.assertEqual(block_to_block_type(h5), block_type_heading)
        self.assertEqual(block_to_block_type(h6), block_type_heading)
        self.assertEqual(block_to_block_type(not_heading), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_heading2), block_type_paragraph)

    def test_block_to_block_type_code(self):
        code = "```python\nprint('Hello, World!')\n```"
        not_code = "```python\nprint('Hello, World!')"
        not_code2 = "``print('Hello, World!')\n```"

        self.assertEqual(block_to_block_type(code), block_type_code)
        self.assertEqual(block_to_block_type(not_code), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_code2), block_type_paragraph)

    def test_block_to_block_type_quote(self):
        quote = "> This is a quote"
        not_quote = ">This is not a quote"
        not_quote2 = "> This is not a quote\nThis is the next line\n> This is another non quote line"

        self.assertEqual(block_to_block_type(quote), block_type_quote)
        self.assertEqual(block_to_block_type(not_quote), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_quote2), block_type_paragraph)

    def test_block_to_block_type_unordered_list(self):
        ul = "* This is a list\n* with items"
        not_ul = "*This is not a list"
        not_ul2 = "* This is not a list\nThis is the next line\n* This is another non list line"

        self.assertEqual(block_to_block_type(ul), block_type_unordered_list)
        self.assertEqual(block_to_block_type(not_ul), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_ul2), block_type_paragraph)

    def test_block_to_block_type_ordered_list(self):
        ol = "1. This is a list\n2. with items\n3. and more items"
        not_ol = "1.This is not a list"
        not_ol2 = "1. This is not list\n3.This is not a list\n2. This is not a list"

        self.assertEqual(block_to_block_type(ol), block_type_ordered_list)
        self.assertEqual(block_to_block_type(not_ol), block_type_paragraph)
        self.assertEqual(block_to_block_type(not_ol2), block_type_paragraph)

    def test_markdown_to_html_node_paragraph(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


This is a third paragraph with a [link](https://example.com)
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here This is the same paragraph on a new line</p><p>This is a third paragraph with a <a href='https://example.com'>link</a></p></div>")

    def test_markdown_to_html_node_headings(self):
        markdown = """
# This is a heading

##this is not a heading

### This is a heading also
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><h1>This is a heading</h1><p>##this is not a heading</p><h3>This is a heading also</h3></div>")

    def test_markdown_to_html_node_code(self):
        markdown = """
```
// my func so funk
run_this_code()
```
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><pre><code>// my func so funk\nrun_this_code()\n</code></pre></div>")


    def test_markdown_to_html_node_quote(self):
        markdown = """
> This is a quote
> This is another line of the quote

This is a paragraph

> This is not another quote
>since missing space
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><blockquote>This is a quote This is another line of the quote</blockquote><p>This is a paragraph</p><p>> This is not another quote >since missing space</p></div>")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = """
* This is a list
* with items

This is a paragraph

* This is not a list
*since missing space

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><ul><li>This is a list</li><li>with items</li></ul><p>This is a paragraph</p><p><i> This is not a list </i>since missing space</p></div>")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = """
1. This is a list
2. with items
3. and more items

This is a paragraph

1. This is not a list
3. since not in order
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(html, "<div><ol><li>This is a list</li><li>with items</li><li>and more items</li></ol><p>This is a paragraph</p><p>1. This is not a list 3. since not in order</p></div>")
