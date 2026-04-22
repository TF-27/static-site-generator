from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
import unittest

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # 1. Excessive blank lines between blocks
    def test_excessive_blank_lines(self):
        md = """
    Block one




    Block two
    """
        # Should still return two blocks, not empty strings in between
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,["Block one", "Block two"])

    # 2. Leading/trailing whitespace on a block
    def test_leading_trailing_whitespace(self):
        md = """
    Block with leading spaces   

    Another block   
    """
        # .strip() should clean these up
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with leading spaces", "Another block"])

    # 3. Single block, no separators
    def test_single_block(self):
        md = "Just one paragraph with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph with no blank lines"])

    # 4. Empty string input
    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

    # 5. Internal single newlines stay in one block
    def test_single_newlines_within_block(self):
        md = """
    Line one
    Line two
    Line three

    A second block
    """
        # Lines 1-3 should be ONE block, not three
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line one\nLine two\nLine three", "A second block"])

    def test_block_to_block_type(self):
        md = """
    Line one
    Line two
    Line three

    > Hello there!
    > - Obi-wan Kenobi

    ```
    if markdown_block.startswith(("```\n")) and markdown_block.endswith(("```")):
        return BlockType.CODE
    ```

    ###### Five

    - List three
    - List one
    - List two

    1. List one
    2. List two
    3. List three
    """
    
        converted_blocks = markdown_to_blocks(md)

        self.assertEqual(block_to_block_type(converted_blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(converted_blocks[1]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(converted_blocks[2]), BlockType.CODE)
        self.assertEqual(block_to_block_type(converted_blocks[3]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(converted_blocks[4]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(converted_blocks[5]), BlockType.ORDERED_LIST)


def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
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
