import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes



class TestTextNode(unittest.TestCase):
    def test_italic_bookended(self):
        test_node = TextNode("_italic start_ normal text _italic middle_ normal text _italic end_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node],"_", TextType.ITALIC)
        expected = [TextNode("italic start", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic end", TextType.ITALIC)]
        self.assertEqual(split_nodes, expected)

    def test_italic_started(self):
        test_node = TextNode("_italic start_ normal text _italic middle_ normal end", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node],"_", TextType.ITALIC)
        expected = [TextNode("italic start", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal end", TextType.TEXT)]
        self.assertEqual(split_nodes, expected)   

    def test_italic_ended(self):
        test_node = TextNode("Normal start _italic middle_ normal text _italic end_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node],"_", TextType.ITALIC)
        expected = [TextNode("Normal start ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic end", TextType.ITALIC)]
        self.assertEqual(split_nodes, expected)

    def test_bold(self):
        test_node = TextNode("This is normal text with **some bold text in the middle** and normal text at the end", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node],"**", TextType.BOLD)
        expected = [TextNode("This is normal text with ", TextType.TEXT), TextNode("some bold text in the middle", TextType.BOLD), TextNode(" and normal text at the end", TextType.TEXT)]
        self.assertEqual(split_nodes, expected)

    def test_code(self):
        test_node = TextNode("This is text `with some code at the end`", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node], "`", TextType.CODE)
        expected = [TextNode("This is text ", TextType.TEXT), TextNode("with some code at the end", TextType.CODE)]
        self.assertEqual(split_nodes, expected)

    def test_multiple_elements(self):
        test_node1 = TextNode("_italic start_ normal text _italic middle_ normal text _italic end_", TextType.TEXT)
        test_node2 = TextNode("_italic start_ normal text _italic middle_ normal end", TextType.TEXT)
        test_node3 = TextNode("Normal start _italic middle_ normal text _italic end_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([test_node1, test_node2, test_node3], "_", TextType.ITALIC)
        expected = [
            TextNode("italic start", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic end", TextType.ITALIC),
            TextNode("italic start", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal end", TextType.TEXT),
            TextNode("Normal start ", TextType.TEXT), TextNode("italic middle", TextType.ITALIC), TextNode(" normal text ", TextType.TEXT), TextNode("italic end", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes, expected)


    def test_not_TextType_TEXT(self):
        test_node = TextNode("This is normal text with **some bold text in the middle** and normal text at the end", TextType.BOLD)
        split_nodes = split_nodes_delimiter([test_node],"**", TextType.BOLD)
        self.assertEqual(split_nodes[0], test_node)

# Test for delimiter and TextType matching. Not implemented yet (both in code and test)
#    def test_input_delim(self):
#        test_node = TextNode("Some **bold** text to test", TextType.TEXT)
#        split_nodes = split_nodes_delimiter([test_node], "**" ,TextType.ITALIC)
#        self.assertNotEqual(split_nodes, [TextNode("Some ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text to test", TextType.TEXT)])
#        self.assertEqual(split_nodes, TextNode("Some **bold** text to test", TextType.TEXT))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text one with a [first link](https://linkone.com) and a [second link](https://linktwo.com)"
        )
        self.assertListEqual([("first link","https://linkone.com"), ("second link", "https://linktwo.com")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text one with a ![first image](https://imageone.com) and a ![second image](https://imagetwo.com)"
        )
        self.assertListEqual([("first image","https://imageone.com"), ("second image", "https://imagetwo.com")], matches)

    def test_link__not_detecting_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_image_not__detecting_link(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no images at all image http://image.com", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no images at all image http://image.com", TextType.TEXT)], new_nodes)

    def test_split_no_links(self):
        node = TextNode("This is text with no links at all link http://link.com", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no links at all link http://link.com", TextType.TEXT)], new_nodes)

    def test_one_image(self):
        node = TextNode("This is only ![one](http://image.com) image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is only ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "http://image.com"),
                TextNode(" image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_one_link(self):
        node = TextNode("This is only [one](http://link.com) link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is only ", TextType.TEXT),
                TextNode("one", TextType.LINK, "http://link.com"),
                TextNode(" link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_ends_with_image(self):
        node = TextNode("This ends with an ![image](http://image.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This ends with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "http://image.com"),
            ],
            new_nodes,
        )

    def test_ends_with_link(self):
        node = TextNode("This ends with a [link](http://zelda.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This ends with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://zelda.com"),
            ],
            new_nodes,
        )

    def test_starts_with_image(self):
        node = TextNode("![start](http://kylo.com) this started with an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "http://kylo.com"),
                TextNode(" this started with an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_starts_with_link(self):
        node = TextNode("[start](http://windwaker.com) this started with a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "http://windwaker.com"),
                TextNode(" this started with a link", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_not_TextTypeTEXT_image(self):
        node = TextNode("Wrong type of node", TextType.LINK, "https://wrongtype.com")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_not_TextTypeTEXT_link(self):
        node = TextNode("Wrong type of node", TextType.LINK, "https://wrongtype.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_text_to_textnodes(self):
        text_in = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test = text_to_textnodes(text_in)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(test, expected)

# Three test provided by boots after I checked the exercise:
    def test_text_to_textnodes_plain_text(self):
        text = "just plain text"
        expected = [TextNode("just plain text", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_bold_only(self):
        text = "hello **world**"
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_multiple_links_and_images(self):
        text = "A [link](https://a.com) and ![img](https://b.com/img.png)"
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://b.com/img.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

# Continuation of own code: