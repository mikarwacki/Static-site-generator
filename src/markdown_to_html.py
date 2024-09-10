import os
from block_markdown import markdown_to_html_node, extract_title

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
            print(html_lines[i])
        if html_lines[i].strip() == "{{ Content }}":
            html_lines[i] = html_from_markdown.to_html()
    
    print(html_lines)
    
    markdown_file.close()
    html_template.close()
    if not os.path.exists(dest_path):
        os.mkdir(dest_path, "w")
    index_file = open(f"{dest_path}/index.html", "w")
    html_lines = "\n".join(html_lines)
    index_file.write(html_lines)



