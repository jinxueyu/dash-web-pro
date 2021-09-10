import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

check_config = {
    "tag_name": "div",
    "attrs": {
        'className': 'className',
        'inputClassName': 'inputClassName',
        'inputStyle': {'a':'ssss'},
        'labelClassName': 'labelClassName',
        'options': [
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
                {"label": "Disabled Option", "value": 3, "disabled": True},
            ],
        'value': [1],
        'id': 'check_list_id'
    }
}
_check_config = check_config['attrs']

clist = dbc.Checklist(**_check_config)
_check_config['id'] = '123344444'
print(clist)

collapse = html.Div(
    [
        clist,
        dbc.Button(
            "Open collapse",
            id="collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse",
            is_open=False
        ),
        html.Div([
            html.Button('Button 1', id='btn-1'),
            html.Button('Button 2', id='btn-2'),
            html.Button('Button 3', id='btn-3'),
            html.Div(id='container')
        ]),
        html.Div(html.Button(id='text_input', children='78888')),
        dcc.Link('页面B', href='/pageB'),
        html.Form([dcc.Input(id='test', value='123')]),
        dcc.Checklist(**check_config['attrs'])
    ]
)

app.layout = dbc.Container(
    [
        dcc.Location(id='url'),
        html.Ul(id='output-url'),
        collapse
    ],
    style={
        'paddingTop': '100px'
    }
)


@app.callback(
    Output('output-url', 'children'),
    [Input('url', 'href'),
     Input('url', 'pathname'),
     Input('url', 'search'),
     Input('url', 'hash')]
)
def show_location(href, pathname, search, hash):
    return (
        html.Li(f'当前href为：{href}'),
        html.Li(f'当前pathname为：{pathname}'),
        html.Li(f'当前search为：{search}'),
        html.Li(f'当前hash为：{hash}')
    )


@app.callback(
    Output("collapse", "is_open"),
    Output('text_input', 'value'),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    print('-----', n, is_open)
    if n:
        return not is_open, str(n)
    return is_open, str(n)


import json


@app.callback(Output('container', 'children'),
              Input('btn-1', 'n_clicks'),
              Input('btn-2', 'n_clicks'),
              Input('btn-3', 'n_clicks'),
              Input('text_input', 'value'))
def display(btn1, btn2, btn3, value):
    ctx = dash.callback_context
    print('trigger', ctx.triggered, btn1, btn2, btn3, value)
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs,
        'value trigger': value
    }, indent=2)

    return html.Div([
        html.Table([
            html.Tr([html.Th('Button 1'),
                     html.Th('Button 2'),
                     html.Th('Button 3'),
                     html.Th('Most Recent Click')]),
            html.Tr([html.Td(btn1 or 0),
                     html.Td(btn2 or 0),
                     html.Td(btn3 or 0),
                     html.Td(button_id)])
        ]),
        html.Pre(ctx_msg)
    ])

print('..start...')

if __name__ == '__main__':
    app.run_server(debug=True)

