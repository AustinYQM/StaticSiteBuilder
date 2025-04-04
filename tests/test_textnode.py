import unittest

from textnode import TextType, TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link node", TextType.LINK, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), f'TextNode(This is a text node, bold, {None})')


if __name__ == "__main__":
    unittest.main()
