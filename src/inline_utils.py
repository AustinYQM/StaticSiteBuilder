from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
import re

def text_node_to_html_node(node: TextNode) -> HTMLNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case _:
            raise Exception(f"Unknown TextType: {node.text_type}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        elif node.text.find(delimiter) != -1:
            split = node.text.split(delimiter, maxsplit=2)
            if len(split) < 3:
                raise Exception(f"Invalid markdown, missing delimiter: {delimiter}")
            new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(split[1], text_type))
            new_nodes.extend(split_nodes_delimiter([TextNode(split[2], TextType.TEXT)], delimiter, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue
        elif len(extract_markdown_images(node.text)) == 0:
            new_nodes.append(node)
        else:
            match = extract_markdown_images(node.text)[0]
            tag = f"![{match[0]}]"
            if node.text.find(tag) != 0:
                new_nodes.append(TextNode(node.text[:node.text.find(tag):], TextType.TEXT))
                new_nodes.extend(split_nodes_image([TextNode(node.text[node.text.find(tag):], TextType.TEXT)]))
            elif node.text.find(tag) == 0:
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
                new_nodes.extend(split_nodes_image([TextNode(node.text[node.text.find(f"({match[1]})")+len(f"({match[1]})"):], TextType.TEXT)]))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue
        elif len(extract_markdown_links(node.text)) == 0:
            new_nodes.append(node)
        else:
            match = extract_markdown_links(node.text)[0]
            tag = f"[{match[0]}]"
            if node.text.find(tag) != 0:
                new_nodes.append(TextNode(node.text[:node.text.find(tag):], TextType.TEXT))
                new_nodes.extend(split_nodes_link([TextNode(node.text[node.text.find(tag):], TextType.TEXT)]))
            elif node.text.find(tag) == 0:
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
                new_nodes.extend(split_nodes_link([TextNode(node.text[node.text.find(f"({match[1]})")+len(f"({match[1]})"):], TextType.TEXT)]))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    return link

def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[([^[]+)]\(([0-9a-zA-Z$\-_.+!*',;/?:@=&]+)\)", text)

def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^[]+)]\(([0-9a-zA-Z$\-_.+!*',;/?:@=&\"]+)\)", text)