from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        node_list = []
 #       print(f"THIS IS A NODE NAMED {node}")
 #       print(f"THIS IS THE NODE'S TEXTTYPE: {node.text_type}")
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

# Testing for unmatched/closing delimiters
        delimiter_count = 0
        if delimiter != "**":
            for letter in node.text:
                if letter == delimiter:
                    delimiter_count += 1

        else:          
            for i in range(1,len(node.text)):
                #print(f"This is the node value/letter: {node.text[i]}")
                if node.text[i] == "*" and node.text[i-1] == "*":
                    delimiter_count += 1
            #print(f"bold delimiter count: {delimiter_count}")
            #print(f"this is the delimiter: {delimiter}")

        if delimiter_count % 2 != 0:
            raise Exception("Unmatched delimiter (no closing delimiters)")

# Splitting the text
        opened = node.text.split(delimiter)

        for i in range(0, len(opened)):
            if opened[i] == "":
                continue
            if i % 2 != 0:
                new_item = TextNode(opened[i], text_type)
                node_list.append(new_item)
            else:
                new_item = TextNode(opened[i], TextType.TEXT)
                node_list.append(new_item)

        new_list.extend(node_list)
    return new_list
            
def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    #return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # Course solution

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    #return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) #course solution


def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        remaining = node.text
        extracted = extract_markdown_images(node.text)
        if extracted == []:
            new_list.append(node)
            continue
        for image in extracted:
            sections = remaining.split(f"![{image[0]}]({image[1]})", 1)
            remaining = sections[1]
            if sections[0] != "":
                new_node1 = TextNode(sections[0], TextType.TEXT)
                new_list.append(new_node1)
            new_node2 = TextNode(image[0], TextType.IMAGE, image[1])
            new_list.append(new_node2)
        if remaining != "":
            last_node = TextNode(remaining, TextType.TEXT)
            new_list.append(last_node)
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        remaining = node.text
        extracted = extract_markdown_links(node.text)
        if extracted == []:
            new_list.append(node)
            continue
        for link in extracted:
            sections = remaining.split(f"[{link[0]}]({link[1]})", 1)
            remaining = sections[1]
            if sections[0] != "":
                new_node1 = TextNode(sections[0], TextType.TEXT)
                new_list.append(new_node1)
            new_node2 = TextNode(link[0], TextType.LINK, link[1])
            new_list.append(new_node2)
        if remaining != "":
            last_node = TextNode(remaining, TextType.TEXT)
            new_list.append(last_node)
    return new_list

#TextNode input: self, text, text_type, url=None

def text_to_textnodes(text):
    nodes_in = [TextNode(text, TextType.TEXT)]
    nodes_output = split_nodes_delimiter(nodes_in, "**", TextType.BOLD)
    nodes_output = split_nodes_delimiter(nodes_output, "_", TextType.ITALIC)
    nodes_output = split_nodes_delimiter(nodes_output, "`", TextType.CODE)
    nodes_output = split_nodes_image(nodes_output)
    return split_nodes_link(nodes_output)
    

#old_nodes, delimiter, text_type
