import json

import requests
from pyquery import PyQuery as pq

dir_url = 'https://marxistphilosophy.org/maozedong/mx%d/index.html'

page_list = range(1, 9)
print(list(page_list))


def request_dir():
    urls = []
    for p in list(range(1, 9)):
        print(p, type(p))
        url = dir_url % (p)
        print('url', url)

        html = pq(url, encoding='gbk')
        items = html('a').items()

        for item in items:
            # print(url[:-10]+item.attr('href'))
            # print(item.text())
            urls.append((str(p)+item.attr('href')[:-4], url[:-10]+item.attr('href')))

    return urls


def request_chapter(c_url, chapter):
    html = pq(c_url, encoding='gbk')

    t = html('.tt2')

    center = list(t('center').items())

    title = center[0]('b').text()
    date = ''
    if len(center) > 1:
        date = center[1].text()

    tail = t("font[style='FONT-SIZE: 9pt']")
    notes = tail.text()

    t.remove("font[style='FONT-SIZE: 9pt']")
    t.remove('center')

    content = t.text()

    page = {
        'chapter': chapter,
        'title': title,
        'date': date,
        'content': content,
        'notes': notes
    }
    return page


if __name__ == '__main__':
    # request_dir()

    url = 'https://marxistphilosophy.org/maozedong/mx1/083.htm'
    urls = request_dir()
    writer = open('mzdwj.txt', 'w')
    print(urls)
    for uu in urls:
        print(uu)
        page_content = request_chapter(uu[1], uu[0])
        page_content = json.dumps(page_content)
        writer.write(page_content+'\n')
    writer.close()
