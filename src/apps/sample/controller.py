import dash_echarts

from apps.sample import layout
from core.controller import Controller

from engine.widgets_manager import Widgets
from metronic.widgets.stretch import build_stretch_card


menu_config = [
        {
            'name': 'NLP',
            'id': 'menu_nlp_100',
            'modules': [
                {
                    'name': 'Sample',
                    'id': 11,
                    'icon': 'layout-sidebar',
                    'items': [
                        {
                            'name': '语义1',
                            'id': 111,
                            'icon': 'bullet',
                            'items': [
                                {
                                    'name': 'IDE',
                                    'id': 1111,
                                    'control': 'sample',
                                    'action': 'ide_page',
                                    'icon': 'bullet',
                                }
                            ]

                        },
                        {
                            'name': '语义2',
                            'id': 112,
                            'icon': 'bullet',
                            'control': 'nlp',
                            'action': 'dashboard_page'
                        }
                    ]
                }
            ]
        },
        {
            'name': '句法分析',
            'id': 'menu_nlp_200',
            'modules': []
        },
        {
            'name': '向量技术',
            'id': 'menu_nlp_300',
            'modules': []
        },
        {
            'name': '文本分析',
            'id': 'menu_nlp_400',
            'modules': []
        },
        {
            'name': '知识图谱',
            'id': 'menu_nlp_500',
            'modules': []
        },
]


class SampleController(Controller):
    def __init__(self):
        Controller.__init__(self, 'sample')

    def dash_board_page(self, **kwargs):
        return layout.layout(self.__build_cards_widget(), menu_config)

    def __build_cards_widget(self):

        # from service
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

        # from layout
        chart = dash_echarts.DashECharts(
            option=option,
            # id='echarts',
            style={
                "height": '350px',
            }
        )

        card_widget = Widgets.instance().get_widget('common.stretch_card')
        card00 = card_widget(card_body=chart, id_name='chart001', title='Chart', sub_title='Hi, chart')
        card01 = build_stretch_card()

        card10 = build_stretch_card()
        card11 = build_stretch_card()
        return [
            [card00, card01],
            [card10, card11]
        ]

    def seg_page(self, **kwargs):
        toolbar_title = Widgets.instance().get_widget('wrapper.toolbar_title')
        return layout.container(self.__build_cards_widget()), toolbar_title(title='Hello', sub_title='Nuan')

    def account_basic_info(self, **kwargs):
        return layout.account_basic_info()

    def action(self, market, communication, **kwargs):
        print(' nlp controller >>>>>>>>  req', market, communication)
        backdrop_layout = Widgets.instance().get_widget('common.backdrop')
        return backdrop_layout()

    def ide_page(self):
        # ide_layout = layout.ide_layout()
        return layout.ide_layout('')

    def ide_commit(self, code, **kwargs):
        result = 'hahahahha'
        return result


controller = SampleController()
