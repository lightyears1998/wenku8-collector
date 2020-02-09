import re
import requests


def get_html_encoding(html):
    pattern = '<meta http-equiv="Content-Type" content=".*charset=([^;"]*)'
    result = re.search(pattern, html)
    if result:
        return result.group(1).strip()


def get_html_document(url) -> str:
    with requests.get(url) as res:
        encoding = get_html_encoding(res.text)
        if encoding:
            res.encoding = encoding
        html = res.text
    html = html.replace('\r\n', '\n')
    return html


def get_raw_content(url: str):
    with requests.get(url) as res:
        if res.status_code == 200:
            return res.content
