from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_code = "code"
block_type_heading = "heading"
block_type_quote = "quote"
block_type_ulist = "unorder list"
block_type_olist = "order list"


def markdown_to_blocks(text: str) -> list:
    blocks = text.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        stripped_blocks.append(stripped_block)
    return stripped_blocks


def block_to_block_type(text: str) -> str:
    if (
        text.startswith("# ")
        or text.startswith("## ")
        or text.startswith("### ")
        or text.startswith("#### ")
        or text.startswith("##### ")
        or text.startswith("###### ")
    ):
        return block_type_heading
    lines = text.splitlines()
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return block_type_code

    if text.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if text.startswith("* ") or text.startswith("- "):
        for line in lines:
            if not line.startswith("* ") and not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    number = 1
    if text.startswith(f"{number}. "):
        for line in lines:
            if not line.startswith(f"{number}. "):
                return block_type_paragraph
            number += 1
        return block_type_olist
    return block_type_paragraph


def text_to_children(text: str):
    textNode = text_to_textnodes(text)
    children = []
    for textnode in textNode:
        html = text_node_to_html_node(textnode)
        children.append(html)
    return children


def heading_to_html(block: str) -> object:
    heading_tag = ""
    if block.startswith("# "):
        heading_tag = "h1"
    elif block.startswith("## "):
        heading_tag = "h2"
    elif block.startswith("### "):
        heading_tag = "h3"
    elif block.startswith("#### "):
        heading_tag = "h4"
    elif block.startswith("##### "):
        heading_tag = "h5"
    elif block.startswith("###### "):
        heading_tag = "h6"
    text = block.lstrip("# ")
    children = text_to_children(text)
    htmlnode = ParentNode(heading_tag, children)
    return htmlnode


def paragraph_to_html(block: str) -> object:
    lines = block.splitlines()
    block = " ".join(lines)
    children = text_to_children(block)
    return ParentNode("p", children)


def quote_to_html(block: str) -> object:
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        new_lines.append(line[2:])
    block = " ".join(new_lines)
    children = text_to_children(block)
    return ParentNode("blockquote", children)


def ulist_to_html(block: str) -> object:
    items = block.splitlines()
    children = []
    for item in items:
        inline_childs = text_to_children(item[2:])
        children.append(ParentNode("li", inline_childs))
    return ParentNode("ul", children)


def olist_to_html(block: str) -> object:
    items = block.splitlines()
    children = []
    for item in items:
        inline_childs = text_to_children(item[3:])
        children.append(ParentNode("li", inline_childs))
    return ParentNode("ol", children)


def code_to_html(block: str) -> object:
    children = text_to_children(block[4:-3])
    code_tag = [ParentNode("code", children)]
    return ParentNode("pre", code_tag)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_code:
        return code_to_html(block)
    if block_type == block_type_quote:
        return quote_to_html(block)
    if block_type == block_type_ulist:
        return ulist_to_html(block)
    if block_type == block_type_olist:
        return olist_to_html(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html(block)


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    html = ParentNode("div", children)
    return html

