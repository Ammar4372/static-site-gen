from textnode import (
    TextNode,
    text_type_text,
    text_type_link,
    text_type_image,
    text_type_code,
    text_type_bold,
    text_type_italic,
)
import re


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        splited_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("invalid markdown syntax")
        for i in range(0, len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                splited_nodes.append(TextNode(sections[i], text_type_text))
            else:
                splited_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(splited_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for match in matches:
            sections = text.split(f"![{match[0]}]({match[1]})", maxsplit=1)
            if len(sections) != 2:
                raise Exception("invalid markdown syntax")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_image, match[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for match in matches:
            sections = text.split(f"[{match[0]}]({match[1]})", maxsplit=1)
            if len(sections) != 2:
                raise Exception("invalid markdown syntax")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_link, match[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def extract_markdown_images(text: str) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "_", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

