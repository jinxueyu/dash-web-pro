from dash import html, dcc

from core.app import app

from metronic.callbacks import menu
from apps.chat import callbacks
from apps.nlp import callbacks
from core import callbacks

from apps.nlp import controller as nlp_controller
from apps.chat import controller as chat_controller
from apps.sample import controller as sample_controller

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-translate/app.py

if __name__ == '__main__':
    app.run_server(debug=True)
