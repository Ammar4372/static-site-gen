from htmlnode import LeafNode
import os
import shutil
import pathlib
from block_markdown import markdown_to_html_node
import sys


def copy_files_recursively(source_dir_path: str, dest_dir_path: str):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    if os.path.exists(source_dir_path):
        listdir = os.listdir(source_dir_path)
        for filename in listdir:
            source_path = os.path.join(source_dir_path, filename)
            dest_path = os.path.join(dest_dir_path, filename)
            if os.path.isfile(source_path):
                shutil.copy(source_path, dest_path)
            else:
                copy_files_recursively(source_path, dest_path)


def extract_title(markdown: str):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.startswith("#"):
            return block[2:]
    raise Exception("Every markdown file must have an h1")


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path)
    content = md.read()
    md.close()
    html = markdown_to_html_node(content)
    title = extract_title(content)
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html.to_html())
    template = template.replace("href=/", f'href="{base_path}')
    template = template.replace("src=/", f'src="{base_path}')
    dirs = os.path.dirname(dest_path)
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    output = open(dest_path, "w")
    output.write(template)
    output.close()


def generate_page_recursive(
    content_dir_path: str, template_path: str, dest_dir_path: str, base_path: str
):
    if os.path.exists(content_dir_path):
        dirs = os.listdir(content_dir_path)
        for path in dirs:
            content_path = os.path.join(content_dir_path, path)
            if os.path.isfile(content_path):
                ext = pathlib.Path(content_path).suffix
                if ext == ".md":
                    stem = pathlib.Path(content_path).stem
                    dest_path = os.path.join(dest_dir_path, stem + ".html")
                    print(dest_path)
                    generate_page(content_path, template_path, dest_path, base_path)
            else:
                print(content_dir_path, content_path)
                dest_path = os.path.join(dest_dir_path, path)
                generate_page_recursive(
                    content_path, template_path, dest_path, base_path
                )


def main():
    base_path = "/"
    if len(sys.argv) == 2:
        base_path = sys.argv[1]
    source_path = "static"
    dest_path = "docs"
    content_path = "content"
    template_path = "template.html"
    copy_files_recursively(source_path, dest_path)
    generate_page_recursive(content_path, template_path, dest_path, base_path)
    node1 = LeafNode("p", "this is a paragraph", {"hidden": "true", "color": "black"})
    node1.to_html()


main()
