import unittest

from block_utils import markdown_to_html_node


class TestMD2HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_orderedList(self):
        md = """
1. This item has **bold** text
2. This item has _italic_ text
3. This item has `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This item has <b>bold</b> text</li><li>This item has <i>italic</i> text</li><li>This item has <code>code</code> text</li></ol></div>")

    def test_unorderedList(self):
        md = """
- This item has **bold** text
- This item has _italic_ text
- This item has `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><ul><li>This item has <b>bold</b> text</li><li>This item has <i>italic</i> text</li><li>This item has <code>code</code> text</li></ul></div>")
    def test_headings(self):
        md = """
# h1

## h2

### h3

#### h4

##### h5

###### h6

####### h7 but really paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>h1</h1><h2>h2</h2><h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6><p>####### h7 but really paragraph</p></div>")

    def test_block_quote(self):
        md = """
>This is a blockquote with **bold** text
>and multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a blockquote with <b>bold</b> text and multiple lines</blockquote></div>")

if __name__ == '__main__':
    unittest.main()
