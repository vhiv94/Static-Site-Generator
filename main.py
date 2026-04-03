from genericpath import isdir
from logging import Logger
import os, shutil

from src.md_to_html import markdown_to_html


def main():
    # with open("debug.md", "r") as f:
    #     debug = f.read()
    # print(markdown_to_html(debug).to_html())
    refresh_public("static", "public")

def refresh_public(src, dst):
    src_path_str = os.path.abspath(src)
    dst_path_str = os.path.abspath(dst)

    if os.path.exists(dst_path_str):
        print(f"errasing {dst_path_str}")
        shutil.rmtree(dst_path_str)
    print(f"(re)creating {dst_path_str}")
    os.mkdir(dst_path_str)

    if os.path.exists(src_path_str):
        for file in os.listdir(src_path_str):
            file_path_str = os.path.abspath(f"{src}/{file}")
            file_dst_path_str = os.path.join(f"{dst_path_str}/", file)
            if os.path.isfile(file_path_str):
                print(f"copying {file_path_str} to {dst}")
                shutil.copy(file_path_str, file_dst_path_str)
            else:
                refresh_public(f"{src}/{file}", f"{dst}/{file}")


if __name__ == "__main__":
    main()
