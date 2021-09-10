from dash import html, dcc

from core.app import app

from callbacks import menu
from callbacks import chat
from callbacks import nlp
from core import callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=True)
