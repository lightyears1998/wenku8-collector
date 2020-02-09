import os
import sys
import hashlib


def prepare_catalog_url(url: str):
    return url.strip()


def prepare_chapter_url(catalog_url, chapter_url: str):
    from urllib.parse import urljoin
    return urljoin(catalog_url, chapter_url)


def normalize_filename(filename: str, scheme: str) -> str:
    scheme_suffix = {
        'yaml': 'yml',
        'markdown': 'md'
    }
    suffix = scheme_suffix[scheme]
    return filename if filename.endswith(suffix) else f'{filename}.{suffix}'


def exit_when_file_exists(output_dir):
    if os.path.exists(output_dir):
        print(f"{output_dir}文件已存在。如需更新文件请使用--override参数。")
        sys.exit(1)


def make_output_dir(output_dir):
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass


def count_volumes_and_chapters(novel):
    volume_count, chapter_count = 0, 0
    for volume in novel['volumes']:
        volume_count = volume_count + 1
        chapter_count = chapter_count + len(volume['chapters'])
    return volume_count, chapter_count


def get_sha256_hash(stuff: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(stuff.encode(encoding='utf8'))
    return sha256_hash.hexdigest()
