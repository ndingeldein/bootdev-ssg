import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        leafNode = LeafNode("p", "Hello World", {"class": "font-black text-2xl", "id": "123"})
        leafNode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        listItemNode = LeafNode("li", "Item 1")
        listItemNode2 = LeafNode("li", "Item 2")
        listItemNode3 = LeafNode("li", "Item 3")

        ulNode = ParentNode("ul", [listItemNode, listItemNode2, listItemNode3], {"class": "list-disc"})

        containerNode = ParentNode("div", [leafNode, leafNode2, ulNode], {"class": "container", "id": "main-container"})

        self.assertEqual(containerNode.to_html(), "<div class='container' id='main-container'><p class='font-black text-2xl' id='123'>Hello World</p><a href='https://www.google.com'>Click me!</a><ul class='list-disc'><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

        headerNode = LeafNode("header", "This is a header")
        mainNode = ParentNode("main", [containerNode], {"class": "main-content"})
        footerNode = LeafNode("footer", "This is a footer")

        bodyNode = ParentNode("body", [headerNode, mainNode, footerNode], {"class": "antialised scrolling-smooth"})
        self.assertEqual(bodyNode.to_html(), "<body class='antialised scrolling-smooth'><header>This is a header</header><main class='main-content'><div class='container' id='main-container'><p class='font-black text-2xl' id='123'>Hello World</p><a href='https://www.google.com'>Click me!</a><ul class='list-disc'><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div></main><footer>This is a footer</footer></body>")
