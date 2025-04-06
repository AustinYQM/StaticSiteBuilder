from blocknode import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_utils import text_to_textnodes, text_node_to_html_node
import re


def markdown_to_blocks(markdown) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return list(filter(lambda x: not x.isspace(), blocks))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.CODE:
                children.append(block_to_codeblock_node(block))
            case BlockType.PARAGRAPH:
                kids = build_children(block.replace("\n", " "))
                children.append(parent_or_leaf("p", kids, block))
            case BlockType.HEADING:
                match_heading = re.compile(r"(#{1,6}\s)")
                match = match_heading.match(block)
                kids = build_children(block[match.end():])
                children.append(parent_or_leaf(f"h{len(match.group())-1}", kids, block))
            case BlockType.QUOTE:
                stripped_quote = remove_starting_characters(">", block)
                stripped_quote = stripped_quote.replace("\n", " ")
                kids = build_children(stripped_quote)
                children.append(parent_or_leaf("blockquote", kids, block))
            case BlockType.ORDERED_LIST:
                stripped_list = remove_ordered_numbers(block)
                lines = stripped_list.split("\n")
                kids = [parent_or_leaf("li", build_children(line), line) for line in lines]
                children.append(parent_or_leaf("ol", kids, block))
            case BlockType.UNORDERED_LIST:
                stripped_list = remove_starting_characters("- ", block)
                lines = stripped_list.split("\n")
                kids = [parent_or_leaf("li", build_children(line), line) for line in lines]
                children.append(parent_or_leaf("ul", kids, block))
    return ParentNode("div", children)


def block_to_codeblock_node(block: str) -> LeafNode:
    block = block.strip("```")
    block = block.lstrip("\n")
    return LeafNode(None, f"<pre><code>{block}</code></pre>")


def build_children(block: str) -> list[HTMLNode] | bool:
    kids = list(map(text_node_to_html_node, text_to_textnodes(block)))
    if len(kids) > 0:
        return kids
    else:
        return False


def parent_or_leaf(tag: str, kids: list[HTMLNode] | bool, value=None):
    if kids:
        return ParentNode(tag, kids)
    else:
        return LeafNode(tag, value)


def remove_starting_characters(chars: str, block: str) -> str:
    lines = block.split("\n")
    stripped_lines = [line.lstrip(chars) for line in lines]
    return "\n".join(stripped_lines)


def remove_ordered_numbers(block: str) -> str:
    lines = block.split("\n")
    new_lines = []
    for i, line in enumerate(lines, start=1):
        new_lines.append(line.lstrip(f"{i}. "))
    return "\n".join(new_lines)
