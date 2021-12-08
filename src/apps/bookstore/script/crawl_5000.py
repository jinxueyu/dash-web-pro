import json

from pyquery import PyQuery as pq

from apps.bookstore.script.tools import add_book


def request_chapter(url, book_name):
    d = pq(url, encoding='utf8')
    title = d('.grap--h2').text()
    author = d('.rate-holder').text()

    content = ''
    name = None

    obj = {'book_name': book_name, 'title': title, 'author': author}

    i = 0
    for item in list(d('.grap')('div').items())[1:]:
        text = item.text().strip()
        if len(text) == 0:
            continue

        if text.startswith('【'):
            if name is None:
                name = text[1:-1]
                continue

            obj[name] = content
            i += 1

            name = text[1:-1]
            content = ''
        else:
            content += text + '\n'

        obj[name] = content

    return obj


def request_dir(url):
    d = pq(url, encoding='utf8')
    for book in d('article').items():
        book_name = book('h2').text()
        urls = []
        for item in book('a').items():
            urls.append(item.attr('href'))
        yield book_name, urls


def crawl():
    url = 'https://gwgz.5000yan.com/'
    books = request_dir(url)

    writer = open('gwgz.txt', 'w')
    for book in books:
        book_name = book[0]
        urls = book[1]
        for u in urls:
            print(book_name, u)
            chapter = request_chapter(u, book_name)
            chapter = json.dumps(chapter)
            writer.write(chapter + '\n')
    writer.close()


def read_articles():
    reader = open('gwgz.txt', 'r')
    count = 0
    books = {}
    while True:
        line = reader.readline()
        if not line:
            break
        obj = json.loads(line)

        article = {}
        for name, v in obj.items():
            if name == '原文':
                name = 'content'

            if name == '题解':
                name = 'intro'

            if name == '翻译' or name == '译文':
                name = 'translation'

            if name == '解读':
                name = 'notes'

            if name == '注释':
                name = 'footnotes'

            if name == 'book_name':
                continue

            if name == 'author':
                v = v.replace('本文出自：', '')

            article[name] = v

        count += 1
        if obj['book_name'] not in books:
            books[obj['book_name']] = []
        books[obj['book_name']].append(article)

    reader.close()
    return books


if __name__ == '__main__':
    # crawl()
    books = read_articles()
    for name, articles in books.items():
        book = {'name': "古文观止 "+name, 'author': '', 'intro': ''}
        add_book(book, articles)
