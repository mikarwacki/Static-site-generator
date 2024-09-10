import os
from block_markdown import markdown_to_html_node 

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(dir_path_content)
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return 
    dir_items = os.listdir(dir_path_content)
    for item in dir_items:
        if os.path.isfile(f"{dir_path_content}/{item}"):
           generate_pages_recursive(f"{dir_path_content}/{item}", template_path, dest_dir_path)
        else:
            generate_pages_recursive(f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_text = markdown_file.read()
    html_template = open(template_path)
    html_file = html_template.read()

    html_from_markdown = markdown_to_html_node(markdown_text)
    title = extract_title(markdown_text)

    html_lines = html_file.split("\n")
    for i in range(len(html_lines)):
        if html_lines[i].lstrip().startswith("<title>"):
            html_lines[i] = html_lines[i].replace('{{ Title }}', title)
        if html_lines[i].strip() == "{{ Content }}":
            html_lines[i] = html_from_markdown.to_html()
    
    markdown_file.close()
    html_template.close()
    if not os.path.exists(dest_path):
        print(dest_path)
        os.mkdir(dest_path)
    index_file = open(f"{dest_path}/index.html", "w")
    html_lines = "\n".join(html_lines)
    print(html_lines)
    index_file.write(html_lines)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == '#':
            return line[2:]
    raise Exception("there is no header")

