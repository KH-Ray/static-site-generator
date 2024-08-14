import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "h1",
            "Heading 1",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            "h1",
            "Heading 1",
            [HTMLNode("p", "Paragraph", None, None)],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        result = "HTMLNode(h1, Heading 1, [HTMLNode(p, Paragraph, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(result, repr(node))

    def test_to_html(self):
        node = HTMLNode("h1", "Heading 1", None, None)
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_LeafNode_exist(self):
        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual("p", node.tag)
        self.assertEqual("This is a paragraph of text.", node.value)
        self.assertEqual(None, node.props)

    def test_to_html(self):
        node = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com", "target": "_blank"}
        )
        result = '<a href="https://www.google.com" target="_blank">Click me!</a>'

        self.assertEqual(result, node.to_html())


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(result, node.to_html())

    def test_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(
                    "a",
                    "Click me!",
                    {"href": "https://www.google.com", "target": "_blank"},
                ),
            ],
        )
        result = '<p><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com" target="_blank">Click me!</a></p>'

        self.assertEqual(result, node.to_html())

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
