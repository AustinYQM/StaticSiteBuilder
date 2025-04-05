def markdown_to_blocks(markdown)-> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return list(filter(lambda x: not x.isspace(), blocks))