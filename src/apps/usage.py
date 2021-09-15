
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from dash_svg_component import Svg

app = dash.Dash(__name__)

svg = Svg(
        src='assets/Code.svg'
    )

app.layout = html.Div([
    html.Div('hi', id='output'),
    html.Div(svg, id='svg')
])


if __name__ == '__main__':
    app.run_server(debug=True)
