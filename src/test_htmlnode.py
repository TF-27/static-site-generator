import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        props = {
            "href": "https://www.starwars.com",
            "target": "_blanc",
        }
        node = HTMLNode("p", "testing this value", None, props)
        node2 = HTMLNode("p", "fucked up", None, props)
        self.assertNotEqual(node,node2)

    def test_props_to_html(self):
        props = {
            "href": "https://www.starwars.com",
            "target": "_bobafett",
        }
        node = HTMLNode("p", "testing this value", None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.starwars.com" target="_bobafett"')

    def test_no_input(self):
        empty_node = HTMLNode()
        self.assertEqual(empty_node.tag, None)
        self.assertEqual(empty_node.value, None)
        self.assertEqual(empty_node.children, None)
        self.assertEqual(empty_node.props, None)

    def test_to_html(self):
        node = HTMLNode("p", "testing this value", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()
    

# Testing leaf nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_value_None(self):
        noval_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            noval_node.to_html()

    def test_link(self):
        link_node = LeafNode("a", "Ride me!", {"href": "https://Excaliber-9.com"})
        self.assertEqual(link_node.to_html(), '<a href="https://Excaliber-9.com">Ride me!</a>')

    def test_link_multitag(self):
        props = props = {
            "href": "https://www.trekbikes.com",
            "target": "_Fuel-EX",
        }
        multitag_node = LeafNode("a", "Modulate me!", props)
        self.assertEqual(multitag_node.to_html(), '<a href="https://www.trekbikes.com" target="_Fuel-EX">Modulate me!</a>')

# Testing parent nodes
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multichild(self):
        child1 = LeafNode("a", "MTB-Life!", {"href": "https://www.https://www.anturstiniog.com"})
        child2 = LeafNode("b", "Go to Wales")
        child3 = LeafNode(None, " to ")
        child4 = LeafNode("i", "downhill in snowdonia")
        parent_node = ParentNode("p",[child1, child2, child3, child4])
        expected = '<p><a href="https://www.https://www.anturstiniog.com">MTB-Life!</a><b>Go to Wales</b> to <i>downhill in snowdonia</i></p>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_childless(self):
        parent_node = LeafNode("div", [])
        parent_node2 = LeafNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
            parent_node2.to_html()

    def test_parentception(self):
        child = LeafNode("b", "Hello there!")
        child_parent = ParentNode("p", [child])
        parent_parent = ParentNode("div", [child_parent])
        self.assertEqual(parent_parent.to_html(), "<div><p><b>Hello there!</b></p></div>")





if __name__ == "__main__":
    unittest.main()

