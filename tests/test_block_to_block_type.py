import unittest

from blocknode import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # Testing heading block
    def test_h1_heading(self):
        block: str = "# H1 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h2_heading(self):
        block: str = "## H2 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h3_heading(self):
        block: str = "### H3 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h4_heading(self):
        block: str = "#### H4 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h5_heading(self):
        block: str = "##### H5 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h6_heading(self):
        block: str = "###### H6 Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_h7_heading_is_paragraph(self):
        block: str = "####### H7 Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    # Testing code block
    def test_code(self):
        block = "```\nThis is a code block \nThis is another line\n```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_oneline_code(self):
        block = "```This is a code block. This is another line```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_midsentence_close_still_code(self):
        block = "```This ```is a code block. This is another line```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_midsentence_code_is_paragraph(self):
        block = "This ```is a code block. This is another line```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    # Testing quote block
    def test_oneline_quote(self):
        block = ">Quotes start with arrows"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_multiline_quote(self):
        block = ">Quotes start with arrows\n>Some have two lines\n>Some have more"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_broken_quote_is_paragraph(self):
        block = ">Quotes start with arrows\nThis isn't a quote\n>because it's missing an arrow in the middle"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    # Testing unordered list
    def test_unordered_list(self):
        block = "- thing1\n- thing2\n- thing3"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_unordered_list_spaces_matter(self):
        block = "-thing1\n- thing2\n- thing3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_unordered_list_break_is_paragraph(self):
        block = "- thing1\nthing2\n- thing3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    # Testing ordered list
    def test_ordered_list(self):
        block = "1. thing1\n2. thing2\n3. thing3"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ordered_no_missing_no(self):
        block = "1. thing1\n thing2\n3. thing3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_ordered_number_order_matters(self):
        block = "2. thing1\n1. thing2\n3. thing3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_ordered_spaces_matters(self):
        block = "1. thing1\n2.thing2\n3. thing3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == '__main__':
    unittest.main()
