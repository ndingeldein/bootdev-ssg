import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "click me", [], {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href='https://example.com' target='_blank'")

        node_no_props = HTMLNode("a", "click me", [])
        self.assertEqual(node_no_props.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("a", "click me", [], {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(repr(node), "HTMLNode(a, click me, [], {'href': 'https://example.com', 'target': '_blank'})")
