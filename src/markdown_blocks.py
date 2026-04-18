from enum import Enum
import re


def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = []
    split_up = markdown.split("\n\n")
    for string in split_up:
        split2 = [line.strip() for line in string.split("\n")]
        split2 = [line for line in split2 if line != ""]
        re_n = "\n".join(split2)
        if re_n.strip() != "":
            blocks.append(re_n)


    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if markdown_block.startswith(("```\n")) and markdown_block.endswith(("```")):
        return BlockType.CODE

#split open for multiple check runs
    split = markdown_block.split("\n")

    quote_check = True
    for line in split:
        if not line.startswith(">"):
            quote_check = False
    if quote_check:
        return BlockType.QUOTE

    ul_check = True
    for line in split:
        if not line.startswith("- "):
            ul_check = False
    if ul_check:
        return BlockType.UNORDERED_LIST

    ol_check = True
    for i in range(0, len(split)):
        if not split[i].startswith(f"{i+1}. "):
            ol_check = False
    if ol_check:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    

    