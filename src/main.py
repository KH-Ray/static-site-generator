from copy_files import copy_static_files
from page_generation import generate_pages_recursive


def main():
    copy_static_files()
    generate_pages_recursive("content", "template.html", "public")


main()
