import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_repr(self):
        node = HTMLNode("a", props={"href": "www.google.com"})
        self.assertEqual(str(node), 'HTMLNode(a, None, None,  href="www.google.com")')
        # add assertion here


if __name__ == '__main__':
    unittest.main()
