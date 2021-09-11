import dash
import dash_ace
import dash_html_components as html
import flask
from flask import jsonify
from flask_cors import CORS

server = flask.Flask(__name__)
CORS(server)

app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/dash/'
                )

app.layout = html.Div([
    dash_ace.DashAceEditor(
        id='input',
        value='def test(a: int) -> str : \n'
              '    return f"value is {a}"',
        theme='monokai',
        mode='python',
        tabSize=4,
        enableBasicAutocompletion=True,
        enableLiveAutocompletion=True,
        autocompleter='/autocompleter?prefix=',
        placeholder='Python code ...'
    )
])


@server.route('/autocompleter', methods=['GET'])
def autocompleter():
    print('-->', )
    return jsonify([{"name": "Completed", "value": "Completed", "score": 100, "meta": "test"}])


if __name__ == '__main__':
    app.run_server(debug=True)
