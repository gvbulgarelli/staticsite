import os
from markdown_to_html import *

def generate_page(from_path, template_path, dest_path):
    """
    Generates an HTML page from a markdown file and a template.
    :param from_path: The path to the markdown file.
    :param template_path: The path to the HTML template file.
    :param dest_path: The destination path to write the generated HTML file.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the HTML template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert markdown to HTMLNode structure
    html_node = markdown_to_html_node(markdown_content)

    # Convert the HTMLNode to HTML string
    html_content = html_node.to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_content)

    print(f"Page generated at {dest_path}")
