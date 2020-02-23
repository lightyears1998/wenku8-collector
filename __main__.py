import os
import sys

import click

from wenku8collector.crawler import get_html_document, get_raw_content
from wenku8collector.packager import pack_pandoc_markdown_scheme, pack_volumed_pandoc_markdown_scheme
from wenku8collector.packager import pack_yaml_scheme, pack_markdown_scheme
from wenku8collector.parser import parse_catalog_page, parse_chapter_page
from wenku8collector.util import count_volumes_and_chapters, get_local_image_filename
from wenku8collector.util import normalize_filename, exit_when_file_exists, make_output_dir
from wenku8collector.util import prepare_catalog_url, prepare_chapter_url


@click.command()
@click.argument('CATALOG_URL')
@click.option('--standalone-volume/--no-standalone-volume',
              default=False, help='指定是否分卷输出，默认不分卷。')
@click.option('--scheme',
              type=click.Choice(['yaml',
                                 'markdown',
                                 'pandoc-markdown'],
                                case_sensitive=False),
              default='yaml',
              help='指定输出文件类型。')
@click.option('--output-dir', type=click.Path(), default='.', help='指定输出目录。')
@click.option('--filename', default=None, help='指定输出文件名。')
@click.option('--override', is_flag=True, default=False, help='覆盖已有文件。')
def main(
        catalog_url: str,
        standalone_volume: bool,
        scheme: str,
        output_dir: str = '',
        filename: str = '',
        override: bool = False):
    """Wenku8Collector小说缓存工具

    将<https://wenku8.net>在线阅读的小说内容缓存为本地EPUB文件。

    \b
    * `CATALOG_URL`必须为小说目录页，形如：<https://www.wenku8.net/novel/0/1/index.htm>。
    """

    # 检查参数
    if scheme == 'yaml':
        if standalone_volume:
            print('以YAML格式输出时忽略`--standalone-volume`参数。')
    elif scheme == 'markdown':
        if standalone_volume:
            print('Markdown格式暂不支持分卷，请使用PandocMarkdown格式。')
            sys.exit(1)

    # 检查输出目录和输出文件名
    if not output_dir:
        output_dir = os.getcwd()
    make_output_dir(output_dir)
    make_output_dir(os.path.join(output_dir, 'images'))
    if filename:
        filename = os.path.join(output_dir, filename)
        filename = normalize_filename(filename, scheme)
        if not override:
            exit_when_file_exists(filename)

    novel = {
        'url': catalog_url,
        'name': 'Unknown',
        'author': 'Unknown',
        'volumes': []
    }

    # 下载元数据
    catalog_url = prepare_catalog_url(catalog_url)
    catalog_html = get_html_document(catalog_url)
    parse_catalog_page(novel, catalog_html)

    print(f'《{novel["name"]}》作者：{novel["author"]}')
    print('共计%s卷，%s节' % count_volumes_and_chapters(novel))

    # 检查输出文件名
    if not filename:
        filename = os.path.join(output_dir, novel['name'])
        filename = normalize_filename(filename, scheme)
        if not override:
            exit_when_file_exists(filename)

    # 下载章节文本
    for volume in novel['volumes']:
        for chapter in volume['chapters']:
            print(f'处理：{volume["name"]}：{chapter["name"]}')
            chapter['url'] = prepare_chapter_url(novel['url'], chapter['url'])
            chapter_html = get_html_document(chapter['url'])
            parse_chapter_page(chapter, chapter_html)

    # 下载图片
    for volume in novel['volumes']:
        for chapter in volume['chapters']:
            for element in chapter['content']:
                if element['type'] == 'image':
                    image_url = element['url']
                    image_local_filename = get_local_image_filename(image_url)
                    image_filename = os.path.join(
                        output_dir, image_local_filename)
                    print(f'处理：{image_url}', end='')
                    if os.path.exists(image_filename):
                        print('（使用缓存）')
                    else:
                        image = get_raw_content(image_url)
                        with open(image_filename, mode='wb') as file:
                            file.write(image)
                        print('（已下载）')

    # 打包
    print(f'打包：{filename}')
    if scheme == 'yaml':
        pack_yaml_scheme(novel, filename)
    elif scheme == 'markdown':
        pack_markdown_scheme(novel, filename)
    elif scheme == 'pandoc-markdown':
        if standalone_volume:
            pack_volumed_pandoc_markdown_scheme(novel, filename)
        else:
            pack_pandoc_markdown_scheme(novel, filename)


if __name__ == '__main__':
    main()
