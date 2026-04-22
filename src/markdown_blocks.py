from enum import Enum
import re
import textnode
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes


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
    

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.PARAGRAPH:
            split_lines = block.split("\n")
            text_to_node = " ".join(split_lines)
            paragraph_html = ParentNode(tag="p", children=text_to_children(text_to_node))
            block_nodes.append(paragraph_html)

        elif block_to_block_type(block) == BlockType.HEADING:
            split = block.split(" ", 1)
            tag = f"h{len(split[0])}"
            heading_html = ParentNode(tag=tag, children=text_to_children(split[1]))
            block_nodes.append(heading_html)
            
        elif block_to_block_type(block) == BlockType.CODE:
            block = block.strip("`")
            block = block.lstrip("\n")
            text_node = TextNode(block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            code_html = ParentNode(tag="code",children=[html_node])
            pre_html = ParentNode(tag="pre", children=[code_html])
            block_nodes.append(pre_html)

        elif block_to_block_type(block) == BlockType.QUOTE:
            split_lines = block.split("\n")
            clean_lines = []
            for line in split_lines:
                clean_lines.append(line[2:])
            text_to_node = " ".join(clean_lines)
            quote_html = ParentNode(tag="blockquote", children=text_to_children(text_to_node))
            block_nodes.append(quote_html)

        elif block_to_block_type(block) in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            split_lines = block.split("\n")
            list_children = []
            for line in split_lines:
                clean_item = line.split(" ", 1)
                child_node = ParentNode(tag="li", children=text_to_children(clean_item[1]))
                list_children.append(child_node)
            tag = "ul" if block_to_block_type(block) == BlockType.UNORDERED_LIST else "ol"
            list_html = ParentNode(tag=tag, children=list_children)
            block_nodes.append(list_html)
  
    return ParentNode(tag="div", children=block_nodes)

    # will Node names conflict in recursion/loop? OR! do I use a function to create children without recursion (in this function at least)


def text_to_children(text): 
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]



    

