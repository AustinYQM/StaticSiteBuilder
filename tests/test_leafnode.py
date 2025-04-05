import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType
from utils import text_node_to_html_node


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "cool site", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">cool site</a>')

    def test_text_to_leaf_txt(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



if __name__ == '__main__':
    unittest.main()
