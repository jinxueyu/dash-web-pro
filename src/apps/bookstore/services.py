import json

from apps.bookstore import dao

bookstore_dao = dao.BookstoreDao('bookstore/bookstore.db')


def get_article(book_id, article_id, page_num):
    article = bookstore_dao.get_article(article_id)

    title = article.title

    content = article.content.split('\n')
    notes = article.notes.split('\n')

    date = article.pub_date
    year_idx = date.find('年')
    month_idx = date.find('月')
    day_idx = date.find('日')
    year = date[:year_idx]
    month = date[year_idx+1:month_idx]
    day = date[month_idx + 1:day_idx]
    date = [year, month, day]

    return {'title': title, 'author': '毛泽东', 'date': date, 'content': content, 'notes': notes}


def get_book(book_id):
    book = bookstore_dao.get_book(book_id)
    catalog = bookstore_dao.get_catalog(book_id)
    return book, catalog


def get_books():
    return bookstore_dao.get_books()
