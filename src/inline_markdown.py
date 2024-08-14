import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for i in range(len(old_nodes)):
        if old_nodes[i].text_type != text_type_text:
            new_nodes.append(old_nodes[i])
            continue

        splitted_texts = old_nodes[i].text.split(delimiter)

        if len(splitted_texts) % 2 == 0:
            raise Exception("no matching closing delimeter")

        for i in range(len(splitted_texts)):
            if splitted_texts[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(splitted_texts[i], text_type_text))
            else:
                new_nodes.append(TextNode(splitted_texts[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            splitted_texts = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(splitted_texts) != 2:
                raise ValueError("image section is not closed properly")

            if splitted_texts[0] != "":
                new_nodes.append(TextNode(splitted_texts[0], text_type_text))

            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            original_text = splitted_texts[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            splitted_texts = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(splitted_texts) != 2:
                raise ValueError("link section is not closed properly")

            if splitted_texts[0] != "":
                new_nodes.append(TextNode(splitted_texts[0], text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = splitted_texts[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def extract_markdown_images(text):
    markdown_images = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    markdown_images.extend(matches)

    return markdown_images


def extract_markdown_links(text):
    markdown_links = []
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    markdown_links.extend(matches)

    return markdown_links


def text_to_textnodes(text):
    node = TextNode(text, text_type_text)

    combined_nodes = []
    nodes_bold = split_nodes_delimiter([node], "**", text_type_bold)
    nodes_italic = split_nodes_delimiter(nodes_bold, "*", text_type_italic)
    nodes_code = split_nodes_delimiter(nodes_italic, "`", text_type_code)
    nodes_image = split_nodes_image(nodes_code)
    nodes_links = split_nodes_links(nodes_image)

    combined_nodes.extend(nodes_links)

    return combined_nodes
