import yaml
from ebooklib import epub
from .util import get_sha256_hash, get_local_image_filename


def pack_yaml_scheme(novel: dict, filename: str):
    with open(filename, 'wb') as file:
        file.write(yaml.dump(novel, allow_unicode=True, encoding='utf8'))


def escape4markdown(text: str) -> str:
    keywords = ['<', '>', '#', '=', '-', '*', '+', '~', '_', '`', '$']
    for keyword in keywords:
        text = text.replace(keyword, '\\' + keyword)
    return text


def pack_markdown_scheme(novel: dict, filename: str):
    with open(filename, 'w', encoding='utf8') as file:
        file.write(f'# {novel["name"]}\n')
        file.write(f'\n作者：{novel["author"]}\n')
        for volume in novel["volumes"]:
            file.write(f'\n## {volume["name"]}\n')
            for chapter in volume["chapters"]:
                file.write(f'\n### {chapter["name"]}\n')
                for element in chapter['content']:
                    if element['type'] == 'text':
                        for paragraph in element['paragraphs']:
                            paragraph = escape4markdown(paragraph)
                            file.write(f'\n{paragraph}\n')
                    elif element['type'] == 'image':
                        url = element['url']
                        image_filename = get_local_image_filename(url)
                        file.write(f'\n![]({image_filename})\n')


def pack_pandoc_markdown_scheme(novel: dict, filename: str):
    with open(filename, 'w', encoding='utf8') as file:
        file.write(f'% {novel["name"]}\n')  # title
        file.write(f'% {novel["author"]}\n')  # author
        for volume in novel["volumes"]:
            file.write(f'\n# {volume["name"]}\n')
            for chapter in volume["chapters"]:
                file.write(f'\n## {chapter["name"]}\n')
                for element in chapter['content']:
                    if element['type'] == 'text':
                        for paragraph in element['paragraphs']:
                            paragraph = escape4markdown(paragraph)
                            file.write(f'\n{paragraph}\n')
                    elif element['type'] == 'image':
                        url = element['url']
                        image_filename = get_local_image_filename(url)
                        file.write(f'\n![]({image_filename})\n')


def pack_volumed_pandoc_markdown_scheme(novel: dict, filename: str):
    for volume in novel["volumes"]:
        sub_filename = f'{filename[:-len(".md")]}：{volume["name"]}.md'
        with open(sub_filename, 'w', encoding='utf8') as file:
            file.write(f'% {novel["name"]}：{volume["name"]}\n')  # title
            file.write(f'% {novel["author"]}\n')  # author
            for chapter in volume["chapters"]:
                file.write(f'\n# {chapter["name"]}\n')
                for element in chapter['content']:
                    if element['type'] == 'text':
                        for paragraph in element['paragraphs']:
                            paragraph = escape4markdown(paragraph)
                            file.write(f'\n{paragraph}\n')
                    elif element['type'] == 'image':
                        url = element['url']
                        image_filename = get_local_image_filename(url)
                        file.write(f'\n![]({image_filename})\n')


def pack_epub_scheme(novel: dict, filename: str):
    # @TODO Bundle EPUB file...

    book = epub.EpubBook()

    book.set_identifier(get_sha256_hash(novel['name']))
    book.set_title(novel['name'])
    book.set_language('zh-CN')
    book.add_author(novel['author'])


if __name__ == '__main__':
    pass
