import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML files for every markdown file in the content directory.
    :param dir_path_content: The path to the content directory.
    :param template_path: The path to the HTML template file.
    :param dest_dir_path: The path to the public directory where the HTML files will be generated.
    """
    for item in os.listdir(dir_path_content):
        src_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        # If the item is a directory, recurse into it
        if os.path.isdir(src_item_path):
            # Recursively create subdirectories in the destination
            os.makedirs(dest_item_path, exist_ok=True)
            generate_pages_recursive(src_item_path, template_path, dest_item_path)
        
        # If the item is a markdown file, generate the corresponding HTML file
        elif os.path.isfile(src_item_path) and src_item_path.endswith(".md"):
            # Convert .md file to .html
            html_file_path = dest_item_path.replace(".md", ".html")
            generate_page(src_item_path, template_path, html_file_path)
            print(f"Generated HTML page: {html_file_path}")
