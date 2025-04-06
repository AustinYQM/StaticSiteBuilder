import logging
import os
import shutil

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler())
logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))

def copy_static_to_public():
    if os.path.exists("public"):
        logger.info("Deleting public folder")
        shutil.rmtree("public")
    if not os.path.exists("public"):
        logger.info("Public folder doesn't exist, creating it.")
        os.mkdir("public")
    static_paths = os.listdir("static")
    # build_dirs(static_paths)
    copy_files(static_paths)

def build_dirs(paths, root: str = ""):
    dirs = list(filter(lambda x: os.path.isdir(os.path.join("static", root, x)), paths))
    for folder in dirs:
        logger.info(f"Creating folder {os.path.join("public", root, folder)}")
        os.mkdir(os.path.join("public", root, folder))
        logger.info(f"Checking for additional folders in {os.path.join("static", root, folder)}")
        build_dirs(os.listdir(os.path.join("static", root, folder)), os.path.join(root, folder))

def copy_files(paths, root: str = ""):
    dirs = list(filter(lambda x: os.path.isdir(os.path.join("static", root, x)), paths))
    files = list(filter(lambda x: os.path.isfile(os.path.join("static", root, x)), paths))
    for file in files:
        logger.info(f"Copying file from {os.path.join("static", root, file)} to {os.path.join("public", root, file)}")
        shutil.copy(os.path.join("static", root, file), os.path.join("public", root, file))
    for folder in dirs:
        logger.info(f"Checking if folder exists at {os.path.join("public", root, folder)}")
        if not os.path.exists(os.path.join("public", root, folder)):
            logger.info(f"Folder does not exist. Creating folder {os.path.join("public", root, folder)}")
            os.mkdir(os.path.join("public", root, folder))
        logger.info(f"Checking for additional files and folders in {os.path.join("static", root, folder)}")
        logger.info(f"Found these files: {os.listdir(os.path.join("static", root, folder))}")
        copy_files(os.listdir(os.path.join("static", root, folder)), os.path.join(root, folder))



def main():
    copy_static_to_public()

main()