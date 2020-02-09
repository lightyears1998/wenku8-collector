import os
import click
from wenku8collector.util import prepare_catalog_url, prepare_chapter_url
from wenku8collector.util import normalize_filename, exit_when_file_exists, make_output_dir
from wenku8collector.util import count_volumes_and_chapters, get_sha256_hash
from wenku8collector.crawler import get_html_document, get_raw_content
from wenku8collector.parser import parse_catalog_page, parse_chapter_page
from wenku8collector.packager import pack_yaml_scheme, pack_markdown_scheme


@click.command()
@click.argument('CATALOG_URL')
@click.option('--scheme',
              type=click.Choice(['yaml', 'markdown'], case_sensitive=False),
              default='yml',
              help='指定输出文件类型。')
@click.option('--output-dir', type=click.Path(), default=None, help='指定输出目录。')
@click.option('--filename', default=None, help='指定输出文件名。')
@click.option('--override', is_flag=True, default=False, help='覆盖已有文件。')
def main(
        catalog_url: str,
        scheme: str,
        output_dir: str = '',
        filename: str = '',
        override: bool = False):
    """<https://wenku8.net>小说缓存工具

    将<https://wenku8.net>在线阅读的小说内容缓存为本地EPUB文件。

    \b
    * `CATALOG_URL`必须为小说目录页，形如：<https://www.wenku8.net/novel/0/1/index.htm>。
    """

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
                    print(f'处理：{image_url}')
                    image_hash_name = get_sha256_hash(image_url)
                    image_filename = os.path.join(output_dir, 'images', image_hash_name)
                    image = get_raw_content(image_url)
                    with open(image_filename, mode='wb') as file:
                        file.write(image)

    # 打包
    if scheme == 'yaml':
        pack_yaml_scheme(novel, filename)
    elif scheme == 'markdown':
        pack_markdown_scheme(novel, filename)


if __name__ == '__main__':
    main()
