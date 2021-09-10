from dash import Output, Input, html, dcc, State, ALL

from core.app import app
from controller.nlp import NlpController

from callbacks import menu
from callbacks import chat
from callbacks import nlp
from core import callbacks

from core import controller
from layouts import login, chat


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=True)
