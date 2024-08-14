import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_image,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_url_exist(self):
        node = TextNode("This is a text node", text_type_bold, "http://www.boot.dev")
        self.assertNotEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        result = "TextNode(This is a text node, text, https://www.boot.dev)"
        self.assertEqual(result, repr(node))

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", text_type_bold))

        self.assertEqual("b", node.tag)
        self.assertEqual("This is a text node", node.value)

    def test_text_node_to_html_node_with_props(self):
        node = text_node_to_html_node(
            TextNode("This is an image", text_type_image, "https://www.boot.dev")
        )

        self.assertEqual("img", node.tag)
        self.assertEqual("This is an image", node.props["alt"])
        self.assertEqual("https://www.boot.dev", node.props["src"])


if __name__ == "__main__":
    unittest.main()
