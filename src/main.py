import os, shutil
from textnode import TextNode
from markdown_to_html import generate_page

public_path = "/home/mikolajkarwacki/static_site_generator/public" 
static_path = "/home/mikolajkarwacki/static_site_generator/static"
from_path = "/home/mikolajkarwacki/static_site_generator/content/index.md"
template_path = "/home/mikolajkarwacki/static_site_generator/template.html"

def copy_contents(path, dest_path):
    if not os.path.exists(path):
        return 
    if os.path.isfile(path):
        shutil.copy(path, dest_path)
        return
    dir_content = os.listdir(path)
    for elem in dir_content:
        if os.path.isdir(path):
            os.mkdir(f"{dest_path}/{elem}")
        copy_contents(f"{path}/{elem}", f"{dest_path}/{elem}")
    return

def main():
    shutil.rmtree(public_path)
    os.mkdir(public_path)
    copy_contents(static_path, public_path)
    generate_page(from_path, template_path, public_path)


main()
