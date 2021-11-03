import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import Output, Input

from apps.bookstore.layout import book_view, article_view, aside_view, store_view

index_string = """<!DOCTYPE html>
<html lang="zh-Hans">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%} 
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

template_name = '../../templates/heti'
app = dash.Dash(__name__,
                index_string=index_string,
                assets_folder=template_name+"/assets",
                assets_url_path="assets",
                # assets_ignore=layout.assets_ignore_str,
                # external_stylesheets=layout.external_stylesheets,
                # external_scripts=layout.external_scripts,
                suppress_callback_exceptions=True,
                prevent_initial_callbacks=True)


# view = article_view(1, 16, 1)
view = store_view()

app.layout = html.Div([
    html.Div([dcc.Location(id='url', refresh=False),
              html.Article(view, id='page-container', className='article heti heti--classic')
              ],
             className='container'
             ),
    html.Div(id='aside-container')]
)


@app.callback(
    Output('page-container', 'children'),
    Output('aside-container', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    print('url click fire:', pathname)
    #   /books/1/chapters/3?page=2
    # 0   1   2   3      4

    if pathname == '' or pathname == '/':
        return store_view(), ''

    arr = pathname.split('?')
    if len(arr) > 1:
        pathname = arr[0]
        params = arr[1]

    page = 1

    path_dict = {

    }
    arr = pathname.split('/')

    for i in range(1, len(arr), 2):
        k = arr[i] if len(arr) > i-1 and len(arr[i]) > 0 else None
        v = arr[i+1] if len(arr) > i and len(arr[i+1]) > 0 else None
        path_dict[k] = v

    chapter_id = path_dict.get('chapters', 0) if 'chapters' in path_dict else None
    book_id = path_dict.get('books', 0) if 'books' in path_dict else None

    book_id = int(book_id) if book_id is not None else None
    chapter_id = int(chapter_id) if chapter_id is not None else None

    if chapter_id is not None:
        return article_view(book_id, chapter_id, page), aside_view(book_id, chapter_id)

    if book_id is not None:
        return book_view(book_id), aside_view(book_id, 1)

    return book_view(1), aside_view(1, 1)


if __name__ == '__main__':
    app.run_server(debug=True)
