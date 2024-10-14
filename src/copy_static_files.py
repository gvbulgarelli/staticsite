import os
import shutil

def copy_static_files(src_dir, dest_dir):
    """
    Recursively copies all contents from src_dir to dest_dir.
    Deletes everything in the dest_dir before copying.
    :param src_dir: The source directory (e.g., 'static')
    :param dest_dir: The destination directory (e.g., 'public')
    """
    # Step 1: Clean the destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)  # Delete the destination directory
    os.mkdir(dest_dir)  # Recreate the destination directory

    # Step 2: Copy all files and directories recursively
    def recursive_copy(src, dest):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if item == "template.html":
                print(f"Skipping {src_path}")
                continue

            if os.path.isdir(src_path):
                # Create directory in the destination
                os.mkdir(dest_path)
                print(f"Directory created: {dest_path}")
                # Recursively copy the contents of the directory
                recursive_copy(src_path, dest_path)
            else:
                # Copy the file to the destination
                shutil.copy(src_path, dest_path)
                print(f"File copied: {dest_path}")

    recursive_copy(src_dir, dest_dir)

if __name__ == "__main__":
    # Source and destination directories
    static_dir = "static"
    public_dir = "public"

    # Copy static files to public directory
    copy_static_files(static_dir, public_dir)
    print("Static files copied successfully!")