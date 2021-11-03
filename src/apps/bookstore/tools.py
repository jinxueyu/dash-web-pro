import json
import re
from apps.bookstore import dao
from apps.bookstore.dao import Book, Article, Catalog


def remove_sup(line):
    return line


def read_articles():
    reader = open('/Users/xueyu/Downloads/mzdwj.txt', 'r')
    count = 0
    articles = {}
    catalog = []
    while True:
        line = reader.readline()
        if not line:
            break
        obj = json.loads(line)

        count += 1
        articles[obj['chapter']] = obj
        catalog.append((obj['chapter'], obj['title']+' -- '+obj['date']))
    reader.close()
    return catalog, articles


def add_book_wenji():
    bookstore_dao = dao.BookstoreDao('bookstore.db')
    bookstore_dao.create_tables()

    books = {}
    catalog, articles = read_articles()
    for k, v in articles.items():
        book_id = k[0]
        if book_id not in books:
            books[book_id] = []
        books[book_id].append(v)

    for book_id, articles in books.items():
        book = Book(name='毛泽东文集（第'+book_id+'部）', author='毛泽东', intro='intro')
        bookstore_dao.write(book)

        for art in articles:
            i = art['notes'].find('\n')
            art['notes'] = re.sub(r'\[\d+\]', '', art['notes'][i + 1:])
            article = Article(author='毛泽东', pub_date=art['date'][1:-1], title=art['title'], content=art['content'], notes=art['notes'][i+1:])
            bookstore_dao.write(article)

            catalog = Catalog(book_id=book.id, chapter_id=article.id, title=remove_sup(article.title))
            bookstore_dao.write(catalog)


if __name__ == '__main__':
    add_book_wenji()
    # book = dao.get_book(1)
    # print(book)
