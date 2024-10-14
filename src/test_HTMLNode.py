import unittest
from HTMLNode import *

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        # Test for props with multiple attributes
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_empty_props(self):
        # Test when props are empty
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        # Test the string representation (__repr__)
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag:a, value:Click here, children:[], props:{'href': 'https://www.example.com'})"
        )

class TestParentNode(unittest.TestCase):

    def test_parentnode_with_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Item 1"),
                LeafNode(None, "Plain text"),
                LeafNode("strong", "Bold text")
            ]
        )
        expected_html = "<div><span>Item 1</span>Plain text<strong>Bold text</strong></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "Bold text")])

    def test_parentnode_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_nested_parentnode(self):
        node = ParentNode(
            "div",
            [
                ParentNode("section", [
                    LeafNode("h1", "Title"),
                    LeafNode(None, "Content")
                ]),
                LeafNode("p", "Paragraph text")
            ]
        )
        expected_html = "<div><section><h1>Title</h1>Content</section><p>Paragraph text</p></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == '__main__':
    unittest.main()
