from lxml import etree


def parse_catalog_page(novel: dict, html: str):
    tree = etree.fromstring(html, parser=etree.HTMLParser())

    novel['name'] = tree.xpath('/html/body/div[@id="title"]')[0].text
    novel['author'] = tree.xpath(
        '/html/body/div[@id="info"]')[0].text.lstrip('作者：')

    volume = None
    for tr in tree.xpath('/html/body/table')[0]:
        for td in tr:
            if etree.iselement(td):
                if td.get('class') == 'vcss':
                    volume = {
                        'name': td.text,
                        'chapters': []
                    }
                    novel['volumes'].append(volume)
                elif td.get('class') == 'ccss':
                    if len(td) > 0:
                        chapter = {
                            'name': td[0].text,
                            'url': td[0].get('href')
                        }
                        if not volume:
                            volume = {
                                'name': '',
                                'chapters': []
                            }
                        volume['chapters'].append(chapter)
    return novel


def parse_chapter_page(chapter: dict, html: str):
    chapter['content'] = []

    tree = etree.fromstring(html, parser=etree.HTMLParser())
    div = tree.xpath('/html/body/div[@id="contentmain"]/div[@id="content"]')[0]
    for tag in div:
        if tag.get('class') == 'divimage':
            image_url = tag[0].get('href')
            chapter['content'].append({
                'type': 'image',
                'url': image_url
            })

        text = tag.tail if tag.tail else ''  # `tag.tail` could be `None`.
        text = text.strip()
        if text:
            if len(chapter['content']
                   ) > 0 and chapter['content'][-1]['type'] == 'text':
                chapter['content'][-1]['paragraphs'].append(text)
            else:
                chapter['content'].append({
                    'type': 'text',
                    'paragraphs': [text]
                })
    return
