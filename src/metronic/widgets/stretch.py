from dash import dcc

from engine.builder import build_tag
import plotly.express as px
import pandas as pd
import dash_echarts

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

df = px.data.gapminder()
fig = px.scatter(df.query("year==2007"),
                 x="gdpPercap",
                 y="lifeExp",
                 size="pop",
                 size_max=60,
                 hover_name="country",
                 log_x=True
                 )


import random
def gen_randlist(num):
    return random.sample(range(num), 7)


option = {
  'xAxis': {
    'data': ['A', 'B', 'C', 'D', 'E']
  },
  'yAxis': {'show': False},
  'series': [
    {
      'type': 'bar',
      'data': [23, 24, 18, 25, 18],
      'barGap': '20%',
      'barCategoryGap': '40%'
    },
    {
      'type': 'bar',
      'data': [12, 14, 9, 9, 11]
    }
  ]
}


chart = dash_echarts.DashECharts(
            option=option,
            # id='echarts',
            style={
                "height": '350px',
            }
        )


stretch_config = {
    "tag_name": "div",
    "attrs": {
        "className": [
            "card",
            "card-xl-stretch",
            "mb-xl-8"
        ]
    },
    "children": [
        {
            "tag_name": "div",
            "attrs": {
                "className": [
                    "card-header",
                    "border-0",
                    "pt-5"
                ]
            },
            "children": [
                {
                    "tag_name": "h3",
                    "attrs": {
                        "className": [
                            "card-title",
                            "align-items-start",
                            "flex-column"
                        ]
                    },
                    "children": [
                        {
                            "tag_name": "span",
                            "attrs": {
                                "className": [
                                    "card-label",
                                    "fw-bolder",
                                    "fs-3",
                                    "mb-1"
                                ]
                            },
                            "children": [
                                "Recent Statistics"
                            ]
                        },
                        {
                            "tag_name": "span",
                            "attrs": {
                                "className": [
                                    "text-muted",
                                    "fw-bold",
                                    "fs-7"
                                ]
                            },
                            "children": [
                                "More than 400 new members"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "tag_name": "div",
            "attrs": {
                "className": [
                    "card-body"
                ]
            },
            "children": [
                {
                    "tag_name": "div",
                    "attrs": {
                        # "id": "kt_charts_widget_1_chart",
                        "style": {"height": "350px"}
                    },
                    "children": [chart
                        # dcc.Graph(
                        # # id='example-graph',
                        # figure=fig)
                    ]
                }
            ]
        }
    ]
}


def build_stretch_card():
    return build_tag(stretch_config)
