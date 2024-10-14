
### Unit Tests:
import unittest
from markdown_to_html import markdown_to_html_node
from HTMLNode import HTMLNode

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_heading(self):
        markdown = "# Heading"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "h1")

    def test_paragraph(self):
        markdown = "This is a paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "p")

    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(node.children[0].children[0].tag, "li")

    def test_code_block(self):
        markdown = "```code```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "pre")

if __name__ == '__main__':
    unittest.main()
