import os, shutil
from textnode import TextNode

public_path = "/home/mikolajkarwacki/static_site_generator/public" 
static_path = "/home/mikolajkarwacki/static_site_generator/static"

def copy_contents(path, dest_path):
    print(path)
    if path == static_path:
        print("in")
        shutil.rmtree(public_path)
        print("deleted public")
        os.mkdir(public_path)
    if not os.path.exists(path):
        return 
    if os.path.isfile(path):
        shutil.copy(path, dest_path)
        return
    dir_content = os.listdir(path)
    for elem in dir_content:
        # path = os.path.join(path, elem)
        if os.path.isdir(path):
            os.mkdir(f"{dest_path}/{elem}")
        print(f"destination path: {dest_path}")
        print(f"elem: {elem}")
        copy_contents(f"{path}/{elem}", f"{dest_path}/{elem}")
    return

def main():
    copy_contents(static_path, public_path)

main()
