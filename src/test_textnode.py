import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode(13233,"italic", "grv.com.br")
        self.assertEqual(node, node2, node3)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, "code")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_bold_delimiter(self):
        node = TextNode("Normal **bold** text", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Normal ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, "italic")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, "text")

    def test_no_delimiter(self):
        node = TextNode("No special formatting here", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "No special formatting here")
        self.assertEqual(new_nodes[0].text_type, "text")

def test_multiple_delimiters(self):
        node = TextNode("Text with **bold** and `code`", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "`", "code")

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, "bold")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, "text")
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, "code")
        self.assertEqual(new_nodes[4].text, "")
        self.assertEqual(new_nodes[4].text_type, "text")


class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "Here is an image ![cat](https://example.com/cat.jpg) and another ![dog](https://example.com/dog.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("cat", "https://example.com/cat.jpg"))
        self.assertEqual(images[1], ("dog", "https://example.com/dog.jpg"))

    def test_extract_markdown_links(self):
        text = "This is a link [Google](https://www.google.com) and another [GitHub](https://www.github.com)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("Google", "https://www.google.com"))
        self.assertEqual(links[1], ("GitHub", "https://www.github.com"))

    def test_extract_empty_text(self):
        text = "This text has no images or links"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(len(images), 0)
        self.assertEqual(len(links), 0)

def test_split_nodes_image(self):
    node = TextNode(
        "Here is an image ![cat](https://example.com/cat.jpg) and more text.",
        "text"
    )
    new_nodes = split_nodes_image([node])
    
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "Here is an image ")
    self.assertEqual(new_nodes[0].text_type, "text")
    self.assertEqual(new_nodes[1].text, "cat")
    self.assertEqual(new_nodes[1].text_type, "image")
    self.assertEqual(new_nodes[1].url, "https://example.com/cat.jpg")
    self.assertEqual(new_nodes[2].text, " and more text.")
    self.assertEqual(new_nodes[2].text_type, "text")

def test_split_nodes_link(self):
    node = TextNode(
        "This is a link [to Google](https://www.google.com) and more text.",
        "text"
    )
    new_nodes = split_nodes_link([node])

    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "This is a link ")
    self.assertEqual(new_nodes[0].text_type, "text")
    self.assertEqual(new_nodes[1].text, "to Google")
    self.assertEqual(new_nodes[1].text_type, "link")
    self.assertEqual(new_nodes[1].url, "https://www.google.com")
    self.assertEqual(new_nodes[2].text, " and more text.")
    self.assertEqual(new_nodes[2].text_type, "text")

def test_split_nodes_no_images_or_links(self):
    node = TextNode("This text has no images or links.", "text")
    new_nodes = split_nodes_image([node])
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text, "This text has no images or links.")
    self.assertEqual(new_nodes[0].text_type, "text")

    new_nodes = split_nodes_link([node])
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text, "This text has no images or links.")
    self.assertEqual(new_nodes[0].text_type, "text")

def test_text_to_textnodes(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    
    self.assertEqual(len(nodes), 10)
    self.assertEqual(nodes[0].text, "This is ")
    self.assertEqual(nodes[0].text_type, "text")
    self.assertEqual(nodes[1].text, "text")
    self.assertEqual(nodes[1].text_type, "bold")
    self.assertEqual(nodes[2].text, " with an ")
    self.assertEqual(nodes[2].text_type, "text")
    self.assertEqual(nodes[3].text, "italic")
    self.assertEqual(nodes[3].text_type, "italic")
    self.assertEqual(nodes[4].text, " word and a ")
    self.assertEqual(nodes[4].text_type, "text")
    self.assertEqual(nodes[5].text, "code block")
    self.assertEqual(nodes[5].text_type, "code")
    self.assertEqual(nodes[6].text, " and an ")
    self.assertEqual(nodes[6].text_type, "text")
    self.assertEqual(nodes[7].text, "obi wan image")
    self.assertEqual(nodes[7].text_type, "image")
    self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
    self.assertEqual(nodes[8].text, " and a ")
    self.assertEqual(nodes[8].text_type, "text")
    self.assertEqual(nodes[9].text, "link")
    self.assertEqual(nodes[9].text_type, "link")
    self.assertEqual(nodes[9].url, "https://boot.dev")

def test_no_formatting(self):
    text = "Just plain text"
    nodes = text_to_textnodes(text)
    
    self.assertEqual(len(nodes), 1)
    self.assertEqual(nodes[0].text, "Just plain text")
    self.assertEqual(nodes[0].text_type, "text")

def test_markdown_to_blocks(self):
    markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 3)
    self.assertEqual(blocks[0], "# This is a heading")
    self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
    self.assertEqual(blocks[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")

def test_empty_lines(self):
    markdown = """
# Heading


This is a paragraph.


"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 2)
    self.assertEqual(blocks[0], "# Heading")
    self.assertEqual(blocks[1], "This is a paragraph.")

def test_no_blocks(self):
    markdown = """
    
    
"""
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(len(blocks), 0)

def test_heading(self):
    block = "# This is a heading"
    self.assertEqual(block_to_block_type(block), "heading")

    block = "### This is a level 3 heading"
    self.assertEqual(block_to_block_type(block), "heading")

def test_code_block(self):
    block = "```\nThis is a code block\n```"
    self.assertEqual(block_to_block_type(block), "code")

def test_quote_block(self):
    block = "> This is a quote\n> Another line of quote"
    self.assertEqual(block_to_block_type(block), "quote")

def test_unordered_list(self):
    block = "* Item 1\n* Item 2"
    self.assertEqual(block_to_block_type(block), "unordered_list")

    block = "- Item A\n- Item B"
    self.assertEqual(block_to_block_type(block), "unordered_list")

def test_ordered_list(self):
    block = "1. First item\n2. Second item"
    self.assertEqual(block_to_block_type(block), "ordered_list")

def test_paragraph(self):
    block = "This is a normal paragraph."
    self.assertEqual(block_to_block_type(block), "paragraph")

if __name__ == "__main__":
    unittest.main()