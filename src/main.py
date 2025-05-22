import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


dir_path_static  = "./static"
dir_path_public  = "./docs"
dir_path_content = "./content"
template_path    = "./template.html"

base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
if not base_path.endswith("/"):
    base_path += "/"


def main():
    print("Deleting docs directory …")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files …")
    copy_files_recursive(dir_path_static, dir_path_public)

    print(f"Generating pages (base-path “{base_path}”) …")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        base_path,
    )


if __name__ == "__main__":
    main()
