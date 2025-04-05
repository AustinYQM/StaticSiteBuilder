import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered-list"
    ORDERED_LIST = "ordered-list"

def block_to_block_type(block: str) -> BlockType | None:
    match_code = re.compile(r"([ ]{0,3}`{3,}[\w\d\s\n]+`{3,})", re.MULTILINE)
    match_heading = re.compile(r"(#{1,6}\s)")
    match_quote = re.compile(r"^>[\w\d\s]+\n?", re.MULTILINE)
    match_unordered_list = re.compile(r"^- [\w\d\s]+\n?", re.MULTILINE)
    # match_ordered_list = re.compile(r"^\d\. [\w\d\s]+\n?", re.MULTILINE)
    if match_heading.match(block):
        return BlockType.HEADING
    elif match_code.match(block):
        return BlockType.CODE
    elif match_quote.match(block):
        return BlockType.QUOTE
    elif match_unordered_list.match(block):
        return BlockType.UNORDERED_LIST


    return None