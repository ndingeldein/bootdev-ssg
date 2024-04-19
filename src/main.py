import os
import shutil

from textnode import TextNode
from block_markdown import (
    markdown_to_html_node,
)

def copy_directory(src, dest):
    list = filter(lambda item: item[0] != ".", os.listdir(src))
    for item in list:
        if os.path.isfile(src + "/" + item):
            shutil.copy(src + "/" + item, dest + "/" + item)
            print(f"Copying {src}/{item} to {dest}/{item}")
        else:
            if not os.path.exists(dest + "/" + item):
                os.makedirs(dest + "/" + item)
                print(f"Creating directory {dest}/{item}")
            copy_directory(src + "/" + item, dest + "/" + item)

def copy_files(static, public):
    if os.path.exists(public):
        shutil.rmtree(public)

    if os.path.exists(static):
        copy_directory(static, public)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        contents = f.read()
        f.close()

    with open(template_path) as f:
        template = f.read()
        f.close()

    body_html = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", body_html)

    with open(dest_path, "x") as f:
         f.write(html)
         f.close()

def generate_pages_recursive(src, template_path, dest):
    list = filter(lambda item: item[0] != ".", os.listdir(src))
    for item in list:
        if os.path.isfile(src + "/" + item) and item.endswith(".md"):
            generate_page(f"{src}/{item}", template_path, f"{dest}/{item[:-3]}.html")
        else:
            if not os.path.exists(dest + "/" + item):
                os.makedirs(dest + "/" + item)
                print(f"Generating pages directory {dest}/{item}")
            generate_pages_recursive(src + "/" + item, template_path, dest + "/" + item)


def main():
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
