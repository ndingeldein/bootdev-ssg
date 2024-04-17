import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html(self):
        node = LeafNode("p", "Hello World", {"class": "font-black text-2xl", "id": "123"})

        self.assertEqual(node.to_html(), "<p class='font-black text-2xl' id='123'>Hello World</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<a href='https://www.google.com'>Click me!</a>")

        node3 = LeafNode(None, "Just a text node")
        self.assertEqual(node3.to_html(), "Just a text node")
