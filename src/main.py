import os, shutil
from markdown_to_html import generate_page, generate_pages_recursive
from copystatic import copy_files_recursive

public_path = "./public" 
static_path = "./static"
from_path = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    print("Copying static files to public directory...")
    copy_files_recursive(static_path, public_path)

    generate_pages_recursive(from_path, template_path, public_path)

main()
