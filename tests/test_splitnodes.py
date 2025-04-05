import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold** text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        print(f"actual: {actual}")
        self.assertEqual(actual, expected)

    def test_double_bold(self):
        node = TextNode("This is **bold** text and so is **this** text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and so is ", TextType.TEXT),
            TextNode("this", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_italics(self):
        node = TextNode("This is _bold_ text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        print(f"actual: {actual}")
        self.assertEqual(actual, expected)

    def test_double_italics(self):
        node = TextNode("This is _bold_ text and so is _this_ text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.ITALIC),
            TextNode(" text and so is ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_code_long(self):
        node = TextNode("This is `a long amount of code` text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a long amount of code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_missing_delimiter(self):
        node = TextNode("This is **bold text.", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)


if __name__ == '__main__':
    unittest.main()
