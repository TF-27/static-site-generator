from textnode import TextNode, TextType
import os
import shutil
from markdown_blocks import markdown_to_html_node
import pathlib
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_log = copy_static_to_main("static", "docs")
    generate_pages_recursive("content","template.html","docs", basepath)
    print(f"file copy log:\n{copy_log}")


def copy_static_to_main(content_path, destination_path):
    shutil.rmtree(destination_path, ignore_errors=True)
    os.mkdir(destination_path)
    file_log = {"new_directory": [], "new_file": []}
    for item in os.listdir(content_path):
        item_path = "/".join([content_path, item])
        item_destination = "/".join([destination_path, item])
        if os.path.isfile(item_path):
            shutil.copy(item_path, item_destination)
            file_log["new_file"].append(item_path)
        else:
            os.mkdir(item_destination)
            file_log["new_directory"].append(item_destination)
            copy_static_to_main(item_path, item_destination)
    return file_log

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.split(" ", 1)
            return title[1].strip()
    raise Exception("No header provided")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}\n")
    with open(from_path, "r") as f:
        file = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_string = markdown_to_html_node(file).to_html()
    title = extract_title(file)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    #print(template)

    if os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content = os.listdir(dir_path_content)
    for item in content:
        item_path = os.path.join(dir_path_content, item)
        #print(f"ITEM PATH: {item_path}")
        if os.path.isfile(item_path):
            if pathlib.Path(item_path).suffix == ".md":
                generate_page(item_path, template_path, os.path.join(dest_dir_path, item.replace(".md", ".html")), basepath)
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)
    




    

main()
