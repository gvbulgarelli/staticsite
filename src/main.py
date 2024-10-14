import shutil
import os
from copy_static_files import copy_static_files
from generate_pages_recursive  import generate_pages_recursive

def main():
    # Clean the public directory
    public_dir = "public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Copy static files
    static_dir = "static"
    copy_static_files(static_dir, public_dir)

    # Generate pages recursively from the content directory
    content_dir = "content"
    template_path = os.path.join(static_dir, "template.html")
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()
