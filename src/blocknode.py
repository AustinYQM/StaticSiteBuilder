import re
from enum import Enum
from functools import reduce


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered-list"
    ORDERED_LIST = "ordered-list"

def block_to_block_type(block: str) -> BlockType | None:
    match_heading = re.compile(r"(#{1,6}\s)")
    lines = block.split("\n")
    oneline = "".join(lines)
    iscode = oneline.startswith("```") and oneline.endswith("```")
    if iscode:
        return BlockType.CODE
    if match_heading.match(lines[0]):
        return BlockType.HEADING
    isquote = reduce(lambda x, y: x and y.startswith(">"), lines, True)
    if isquote:
        return BlockType.QUOTE
    isunordered_list = reduce(lambda x, y: x and y.startswith("- "), lines, True)
    if isunordered_list:
        return BlockType.UNORDERED_LIST
    isordered_list = True
    for i, line in enumerate(lines, start=1):
        isordered_list = isordered_list and line.startswith(f"{i}. ")
    if isordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH