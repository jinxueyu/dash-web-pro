import dash_echarts

from apps.nlp import layout
from core.controller import Controller

from engine.widgets_manager import Widgets
from metronic.widgets.stretch import build_stretch_card


menu_config = [
        {
            'name': 'NLP',
            'id': 1,
            'modules': [
                {
                    'name': 'ide',
                    'id': 'ide',
                    'control': 'nlp',
                    'action': 'ide_page',
                    'icon': 'app-indicator'
                },
                {
                    'name': 'form',
                    'id': 'form01',
                    'control': 'nlp',
                    'action': 'account_basic_info',
                    'icon': 'app-indicator'
                },
                {
                    'name': '语义',
                    'id': 11,
                    'icon': 'layout-sidebar',
                    'items': [
                        {
                            'name': '语义1',
                            'id': 111,
                            'icon': 'bullet',
                            'items': [
                                {
                                    'name': '语义11',
                                    'id': 1111,
                                    'control': 'nlp',
                                    'action': 'lac_page',
                                    'icon': 'bullet',
                                }
                            ]

                        },
                        {
                            'name': '语义2',
                            'id': 112,
                            'control': 'nlp',
                            'action': 'dashboard_page',
                            'icon': 'bullet',
                        }
                    ]
                }
            ]
        },
]


class NlpController(Controller):
    def __init__(self):
        Controller.__init__(self, 'nlp')
        print('nlp controller init...')

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
        toolbar_title = Widgets.instance().get_widget('content.toolbar_title')
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


controller = NlpController()
