import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none(self):
        none1 = TextNode("Testing None input to url", TextType.ITALIC, None)
        none2 = TextNode("Testing None input to url", TextType.ITALIC)
        self.assertEqual(none1, none2)
    
    def test_url(self):
        url1 = TextNode("Testing url not same", TextType.LINK, "kenobi.com")
        url2 = TextNode("Testing url not same", TextType.LINK, "general.com")
        self.assertNotEqual(url1, url2)

    def test_text(self):
        text1 = TextNode("Hello There!", TextType.LINK, "grievous.com")
        text2 = TextNode("General Kenobi!", TextType.LINK, "grievous.com")
        self.assertNotEqual(text1, text2)

    def test_text_type(self):
        type1 = TextNode("Hello There!", TextType.BOLD, "kenobi.com")
        type2 = TextNode("Hello There!", TextType.ITALIC, "kenobi.com")
        self.assertNotEqual(type1, type2)

    def test_double_dif(self):
        double1 = TextNode("Hello There!", TextType.BOLD, "kenobi.com")
        double2 = TextNode("Hello There!", TextType.ITALIC, "grievous.com")
        self.assertNotEqual(double1, double2)

    def triple_double_dif(self):
        triple1 = TextNode("Hello There!", TextType.BOLD, "kenobi.com")
        triple2 = TextNode("You are a bold one!", TextType.ITALIC, "grievous.com")
        self.assertNotEqual(triple1, triple2)

    def test_text_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_conversion(self):
        bold_node = TextNode("This is a bold node", TextType.BOLD)
        bold_html = text_node_to_html_node(bold_node)
        self.assertEqual(bold_html.tag, "b")
        self.assertEqual(bold_html.value, "This is a bold node")

    def test_italic_conversion(self):
        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        italic_html = text_node_to_html_node(italic_node)
        self.assertEqual(italic_html.tag, "i")
        self.assertEqual(italic_html.value, "This is an italic node")

    def test_code_conversion(self):
        code_node = TextNode("This is a code node", TextType.CODE)
        code_html = text_node_to_html_node(code_node)
        self.assertEqual(code_html.tag, "code")
        self.assertEqual(code_html.value, "This is a code node")

    def test_link_conversion(self):
        link_node = TextNode("This is a link node", TextType.LINK, "https://www.inpark.com")
        link_html = text_node_to_html_node(link_node)
        self.assertEqual(link_html.tag, "a")
        self.assertEqual(link_html.value, "This is a link node")
        self.assertEqual(link_html.props, {"href": "https://www.inpark.com"})

    def test_image_conversion(self):
        img_node = TextNode("This is an image node", TextType.IMAGE, "https://www.image.img")
        img_html = text_node_to_html_node(img_node)
        self.assertEqual(img_html.tag, "img")
        self.assertEqual(img_html.value, "")
        self.assertEqual(img_html.props, {"src": "https://www.image.img","alt": "This is an image node"})

    def test_no_text_type(self):
        error_node = TextNode("This is a None TextType", None)
        with self.assertRaises(Exception):
            error_html = text_node_to_html_node(error_node)


if __name__ == "__main__":
    unittest.main()
