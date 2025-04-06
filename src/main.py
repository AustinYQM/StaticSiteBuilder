import http.server
import socketserver
import logging
import os
import shutil
import sys

from block_utils import markdown_to_html_node

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler())
logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))

def copy_static_to_public():
    if os.path.exists("docs"):
        logger.info("Deleting docs folder")
        shutil.rmtree("docs")
    if not os.path.exists("docs"):
        logger.info("Docs folder doesn't exist, creating it.")
        os.mkdir("docs")
    static_paths = os.listdir("static")
    copy_files(static_paths)

def copy_files(paths, root: str = ""):
    dirs = list(filter(lambda x: os.path.isdir(os.path.join("static", root, x)), paths))
    files = list(filter(lambda x: os.path.isfile(os.path.join("static", root, x)), paths))
    for file in files:
        logger.info(f"Copying file from {os.path.join("static", root, file)} to {os.path.join("docs", root, file)}")
        shutil.copy(os.path.join("static", root, file), os.path.join("docs", root, file))
    for folder in dirs:
        logger.info(f"Checking if folder exists at {os.path.join("docs", root, folder)}")
        if not os.path.exists(os.path.join("docs", root, folder)):
            logger.info(f"Folder does not exist. Creating folder {os.path.join("docs", root, folder)}")
            os.mkdir(os.path.join("docs", root, folder))
        logger.info(f"Checking for additional files and folders in {os.path.join("static", root, folder)}")
        logger.info(f"Found these files: {os.listdir(os.path.join("static", root, folder))}")
        copy_files(os.listdir(os.path.join("static", root, folder)), os.path.join(root, folder))

def create_template_replacements(md: str) -> tuple[str, str]:
    title = None
    for line in md.splitlines():
        if line.startswith("#") and not line.startswith("##"):
            title = line[1:].strip()
            break
    if not title:
        raise Exception("markdown should contain h1 for title")
    return title, markdown_to_html_node(md).to_html()

def generate_page(from_path, template_path: str ="template.html", dest_path: str = "docs/index.html", basepath="/"):
    logger.info(f"Generate page from {from_path} to {dest_path} using {template_path}")
    logger.info(f"Attempting to read md file at {from_path}")
    with open(from_path) as f:
        mdfile = f.read()
    logger.info("Extracting title from MD file")
    title, html = create_template_replacements(mdfile)
    logger.info(f"Extracted <Title>: {title}")
    with open(template_path) as f:
        template = f.read()
    template = (template.replace("{{ Title }}", title).replace("{{ Content }}", html) .replace('href="/', f'href="{basepath}')).replace('src="/', f'src="{basepath}')
    dirr = os.path.dirname(dest_path)
    # full_path = os.path.join(dest_path, "index.html")
    logger.info(f"Checking if directory exists at {dirr}")
    if not os.path.exists(dirr):
        logger.info(f"{dirr} did not exist. Creating directory at {dirr}")
        os.makedirs(dirr)
    with open(dest_path, "w") as f:
        logger.info(f"Writing file to {dest_path}")
        f.write(template)

def generate_pages_recursive(content_dir="content", template_path="template.html", dest_path="docs", basepath="/"):
    logger.info(f"Looking at files in {content_dir}")
    content = os.listdir(content_dir)
    logger.info(f"Items found at {content_dir}: {content}")
    for file in content:
        logger.info(f"Processing {file}")
        file_path = os.path.join(content_dir, file)
        target_path = os.path.join(dest_path, file)
        if os.path.isfile(file_path):
            filename = f"{os.path.splitext(target_path)[0]}.html"
            logger.info(f"Generating {file_path} as {filename}")
            generate_page(file_path, template_path, filename, basepath)
        elif os.path.isdir(file_path):
            logger.info(f"Processing files in {file_path} to make pages in {target_path}")
            generate_pages_recursive(file_path, template_path, target_path, basepath)



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    # generate_page("content/index.md", "template.html", "index.html")
    generate_pages_recursive(basepath=basepath)

main()