from HTMLNode import LeafNode
import re

class TextNode:
    def __init__ (self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        
        
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"
    

def text_node_to_html_node(text_node):

    if text_node.text_type == "text":
        return LeafNode(value=text_node.text)  # Raw text node (no tag)
    
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    
    elif text_node.text_type == "link":
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL.")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    
    elif text_node.text_type == "image":
        if not text_node.url:
            raise ValueError("Image TextNode must have a URL.")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    else:
        raise ValueError(f"Unknown TextNode type: {text_node.text_type}")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits text nodes in the old_nodes list based on a delimiter and assigns a new text type.
    :param old_nodes: List of TextNode objects to process.
    :param delimiter: The delimiter that identifies where to split.
    :param text_type: The text type to assign to the split part.
    :return: A new list of TextNode objects, where some may have been split.
    """
    new_nodes = []

    for node in old_nodes:
        # Only process "text" type nodes
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Split the node's text by the delimiter, keeping track of inside/outside delimiter
        parts = node.text.split(delimiter)
        inside_delimiter = False  # This flag tracks whether we're inside the delimiter

        for i, part in enumerate(parts):
            if part or i == len(parts) - 1:  # Add even an empty part at the end
                if inside_delimiter:
                    # Text inside the delimiter should have the new text type
                    new_nodes.append(TextNode(part, text_type))
                else:
                    # Text outside the delimiter remains "text" type
                    new_nodes.append(TextNode(part, "text"))

            # Toggle the flag after each part (alternating between inside and outside)
            inside_delimiter = not inside_delimiter

    return new_nodes

def extract_markdown_images(text):
    """
    Extracts markdown image links from the text.
    :param text: A string containing markdown text.
    :return: A list of tuples where each tuple contains (alt_text, image_url).
    """
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown links from the text.
    :param text: A string containing markdown text.
    :return: A list of tuples where each tuple contains (anchor_text, url).
    """
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches

def split_nodes_image(old_nodes):
    """
    Splits text nodes in the old_nodes list by extracting markdown images.
    :param old_nodes: List of TextNode objects to process.
    :return: A new list of TextNode objects where images are split into separate nodes.
    """
    new_nodes = []

    for node in old_nodes:
        # Only process "text" type nodes
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Extract images from the node's text
        images = extract_markdown_images(node.text)

        # If no images, just append the node
        if not images:
            new_nodes.append(node)
            continue

        # Split the node's text around the images
        text = node.text
        start_idx = 0

        for alt_text, image_url in images:
            # Find the image markdown in the text
            image_markdown = f"![{alt_text}]({image_url})"
            idx = text.find(image_markdown, start_idx)

            # Add the text before the image (if any)
            if idx > start_idx:
                new_nodes.append(TextNode(text[start_idx:idx], "text"))

            # Add the image node
            new_nodes.append(TextNode(alt_text, "image", image_url))

            # Move the start index forward
            start_idx = idx + len(image_markdown)

        # Add any remaining text after the last image
        if start_idx < len(text):
            new_nodes.append(TextNode(text[start_idx:], "text"))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits text nodes in the old_nodes list by extracting markdown links.
    :param old_nodes: List of TextNode objects to process.
    :return: A new list of TextNode objects where links are split into separate nodes.
    """
    new_nodes = []

    for node in old_nodes:
        # Only process "text" type nodes
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Extract links from the node's text
        links = extract_markdown_links(node.text)

        # If no links, just append the node
        if not links:
            new_nodes.append(node)
            continue

        # Split the node's text around the links
        text = node.text
        start_idx = 0

        for anchor_text, link_url in links:
            # Find the link markdown in the text
            link_markdown = f"[{anchor_text}]({link_url})"
            idx = text.find(link_markdown, start_idx)

            # Add the text before the link (if any)
            if idx > start_idx:
                new_nodes.append(TextNode(text[start_idx:idx], "text"))

            # Add the link node
            new_nodes.append(TextNode(anchor_text, "link", link_url))

            # Move the start index forward
            start_idx = idx + len(link_markdown)

        # Add any remaining text after the last link
        if start_idx < len(text):
            new_nodes.append(TextNode(text[start_idx:], "text"))

    return new_nodes


def text_to_textnodes(text):
    """
    Converts markdown text into a list of TextNode objects based on formatting such as bold, italic, code, images, and links.
    :param text: A string containing markdown text.
    :return: A list of TextNode objects.
    """
    # Start with the entire text as a single text node
    nodes = [TextNode(text, "text")]

    # Process images first
    nodes = split_nodes_image(nodes)

    # Process links
    nodes = split_nodes_link(nodes)

    # Process bold text (using ** for bold)
    nodes = split_nodes_delimiter(nodes, "**", "bold")

    # Process italic text (using * for italic)
    nodes = split_nodes_delimiter(nodes, "*", "italic")

    # Process code blocks (using ` for code)
    nodes = split_nodes_delimiter(nodes, "`", "code")

    return nodes

def markdown_to_blocks(markdown):
    """
    Splits the markdown text into individual blocks separated by blank lines.
    :param markdown: A raw markdown string.
    :return: A list of non-empty, trimmed block strings.
    """
    # Split the markdown string by double newlines to get potential blocks
    raw_blocks = markdown.split('\n\n')

    # Strip leading/trailing whitespace from each block and remove empty blocks
    blocks = [block.strip() for block in raw_blocks if block.strip()]

    return blocks

def block_to_block_type(block):
    """
    Determines the type of a markdown block based on its content.
    :param block: A single block of markdown text (stripped of leading/trailing whitespace).
    :return: A string representing the block type.
    """

    # Check for headings (1-6 # characters followed by a space)
    if block.startswith("#"):
        if 1 <= len(block.split(' ')[0]) <= 6 and block.split(' ')[0].startswith("#"):
            return "heading"

    # Check for code blocks (start and end with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return "code"

    # Check for quote blocks (every line starts with '>')
    if all(line.startswith(">") for line in block.splitlines()):
        return "quote"

    # Check for unordered list blocks (every line starts with * or - followed by a space)
    if all(line.startswith("* ") or line.startswith("- ") for line in block.splitlines()):
        return "unordered_list"

    # Check for ordered list blocks (every line starts with a number followed by . and a space)
    lines = block.splitlines()
    if all(line.lstrip().startswith(f"{i}. ") for i, line in enumerate(lines, 1)):
        return "ordered_list"

    # If none of the above, it's a paragraph
    return "paragraph"