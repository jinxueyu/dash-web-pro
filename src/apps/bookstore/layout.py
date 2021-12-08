import re

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from apps.bookstore.services import get_article, get_book, get_books


def add_sup(line):
    items = []
    pre_end = 0
    while True:
        start = line.find('[', pre_end)
        end = line.find(']', pre_end)
        # print(pre_end, start, end)
        if start < 0 or end < 0:
            # print('-----', pre_end, start, end, line[pre_end:])
            items.append(line[pre_end:])
            break
        else:
            idx = line[start + 1:end]
            items.extend([
                line[pre_end:start],
                html.Sup(html.A('[' + idx + ']', href='#fn-' + idx, id='ref-' + idx))
            ])

        pre_end = end+1

    return items


def aside_view(book_id, chapter_id):
    u0 = html.Ul([
        html.Li([dbc.Input(type="radio", className="J_radioGrid"),
                 html.Label(dcc.Link('图书馆', href='/'))])
    ], className='panel-list panel-list--gray')

    u1 = html.Ul([
        html.Li([dbc.Input(type="radio", className="J_radioGrid"),
                 html.Label(dcc.Link('前一章', href='/books/'+str(book_id)+'/chapters/'+str(chapter_id-1)))]),
        html.Li([dbc.Input(type="radio", className="J_radioGrid"),
                 html.Label(dcc.Link('目录', href='/books/'+str(book_id)))]),
        html.Li([dbc.Input(type="radio", className="J_radioGrid"),
                 html.Label(dcc.Link('后一章', href='/books/'+str(book_id)+'/chapters/'+str(chapter_id+1)))]),
    ], className='panel-list panel-list--gray')
    u2 = html.Ul([
        html.Li([dbc.Input(type="radio", className="J_fontStack", value="heti--classic"), html.Label('传统')]),
        html.Li([dbc.Input(type="radio", className="J_fontStack", value="heti--sans"), html.Label('黑体')]),
        html.Li([dbc.Input(type="radio", className="J_fontStack", value="heti--serif"), html.Label('宋体')])
    ], className='panel-list panel-list--gray')
    u3 = html.Ul([
        html.Li([dbc.Input(type="radio", className="J_darkMode", value="auto"), html.Label('🌗', htmlFor='darkmode-auto')]),
        html.Li([dbc.Input(type="radio", className="J_darkMode", value="light"), html.Label('🌞', htmlFor='darkmode-light')]),
        html.Li([dbc.Input(type="radio", className="J_darkMode", value="dark"), html.Label('🌙', htmlFor='darkmode-dark')])
    ], className='panel-list panel-list--gray panel-list--icon')

    return html.Aside([u0, u1, u2, u3], className='panel')


def article_view(book_id, article_id, page_num):

    article = get_article(book_id, article_id, page_num)

    # <h2 id="intro">介绍<a class="anchor" href="#intro">#</a></h2>
    # intro_title = html.H2(
    #     ['介绍', html.A('#', className='anchor', href='#intro')],
    #     id='intro'
    # )
    article_title = html.H1(article['title'], className='article__title')
    intro = html.Blockquote(article['intro'])

    title = html.H1(add_sup(article['title']))
    page_items = [title]

    author_list = []
    if 'author' in article:
        author_list.extend(['作者：', html.Span(article['author'])])

    if 'date' in article and article['date'] is not None:
        year_len = len(article['date'][0])
        month_len = len(article['date'][1])
        day_len = len(article['date'][2])

        date_items = ['（']
        if year_len > 0:
            date_items.extend([html.Span(article['date'][0], className='heti-spacing-start'), '年'])
        if month_len > 0:
            date_items.extend([html.Span(article['date'][1], className='heti-spacing-start'), '月'])
        if day_len > 0:
            date_items.extend([html.Span(article['date'][2], className='heti-spacing-start'), '日'])
        date_items.append('）')

        if len(date_items) > 2:
            author_list.extend(date_items)

    author = html.P(
        author_list,
        className='heti-meta heti-small'
    )

    page_items.append(author)

    content_items = [html.P(add_sup(line)) for line in article['content']]
    page_items.extend(content_items)

    if 'footnotes' in article:
        footnote_items = []
        for idx, line in enumerate(article['footnotes'], start=1):
            if len(line) > 0:
                num = line[1: line.find(']')]
                line = re.sub(r'\[\d+\]', '', line)
                footnote_items.append(html.Li([html.A('^', href="#ref-"+str(num)), line], id='fn-'+str(num)))

        if len(footnote_items) > 0:
            # footnotes = html.Details([
            #     html.Summary('注释', id='footnotes'),
            #
            # ], open=True)
            footnotes = html.Div(html.Ol(footnote_items), className='heti-fn')
            page_items.append(footnotes)

    content_title = html.H2([
        '正文',
        html.A('#', className='anchor', href='#content')
    ], id='content')
    content = html.Section(
        html.Div(page_items, className='heti--ancient'),
        className='demo'
    )

    translation = ''
    if article['translation'] is not None:
        translation_items = [html.P(add_sup(line)) for line in article['translation']]
        translation = html.Details([
            html.Summary('译文', id='translation'),
            html.Section(
                html.Div(translation_items, className='heti--ancient'),
                className='demo'
            )
        ], open=True)
        # translation_title = html.H2([
        #     '译文',
        #     html.A('#', className='anchor', href='#translation')
        # ], id='translation')
        # translation = html.Section(
        #     html.Div(translation_items, className='heti--ancient'),
        #     className='demo'
        # )

    notes = ''
    if article['notes'] is not None:
        notes_items = [html.P(add_sup(line)) for line in article['notes']]
        notes = html.Details([
            html.Summary('解读', id='notes'),
            html.Section(
                html.Div(notes_items, className='heti--ancient'),
                className='demo'
            )
        ], open=True)

    nav_items = [
        html.Li(html.A('介绍', href='#intro')),
        html.Li(html.A([
            '正文',
            html.Ul([html.Li(html.A('注释', href='#footnotes'))])
        ], href='#content')),
        html.Li(html.A('译文', href='#translation')),
        html.Li(html.A('解读', href='#notes')),
    ]

    nav = html.Nav(
        html.Details([
            html.Summary('目录'),
            html.Ol(nav_items)
        ], open=True),
        className='article__nav heti-skip')

    return [article_title, intro, nav, content_title, content, translation, notes]


def book_view(book_id):
    book, catalog = get_book(book_id)
    catalog_items = []
    cat_items = catalog
    for cat in cat_items:
        catalog_items.append(html.Li(
            dcc.Link(cat.title, href='/books/'+str(book_id)+'/chapters/'+str(cat.chapter_id))
        ))

    items = [
        html.H1(book.name, className='article__title'),
        html.Blockquote(book.intro),
        html.Nav(html.Ol(), className='article__nav heti-skip'),
        html.H2(['目录', html.A('#', className='anchor')]),
        html.Ol(catalog_items)
    ]

    return items


def store_view():
    books = get_books()

    book_items = []
    for book in books:
        book_items.append(html.Li(
            dcc.Link(book.name, href='/books/' + str(book.id))
        ))

    items = [
        html.H1('图书馆', className='article__title'),
        html.Blockquote('共有图书' + str(len(books)) + '本'),
        html.Nav(html.Ol(), className='article__nav heti-skip'),
        html.H2(['图书列表', html.A('#', className='anchor')]),
        html.Ol(book_items)
    ]

    return items

