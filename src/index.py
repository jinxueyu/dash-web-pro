from dash import html, dcc

from core.app import app

from metronic.callbacks import menu
from apps.chat import callbacks
from apps.nlp import callbacks
from core import callbacks

from apps.nlp import controller

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=True)
