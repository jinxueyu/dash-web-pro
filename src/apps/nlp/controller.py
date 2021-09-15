import dash_echarts

from apps.nlp import layout, service
from core.controller import Controller

from engine.widgets_manager import Widgets
from metronic.widgets.stretch import build_stretch_card


menu_config = [
        {
            'name': 'NLP',
            'id': 'menu_nlp_100',
            'modules': [
                {
                    'name': '词法分析',
                    'id': 'menu_nlp_101',
                    'icon': 'list-nested',
                    'items': [
                        {
                            'name': '分词',
                            'id': 'menu_nlp_102',
                            'icon': 'bullet',
                            'control': 'nlp',
                            'action': 'seg_layout'
                        },
                        {
                            'name': '词性标注',
                            'id': 'menu_nlp_103',
                            'icon': 'bullet',
                            'control': 'nlp',
                            'action': 'tag_layout'
                        },
                        {
                            'name': '命名实体识别',
                            'id': 'menu_nlp_104',
                            'icon': 'bullet',
                            'control': 'nlp',
                            'action': 'ner_layout'
                        },
                    ]
                },
                {
                    'name': '句法分析',
                    'id': 'menu_nlp_200',
                    'icon': 'blockquote-left',
                    'items': [
                        {
                            'name': '句法依存分析',
                            'id': 'menu_nlp_201',
                            'icon': 'bullet',
                            'control': 'nlp',
                            'action': 'ddp_layout'
                        },
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


class NlpController(Controller):
    def __init__(self):
        Controller.__init__(self, 'nlp')

    def index_layout(self):
        return layout.index(menu_config)

    def seg_layout(self):
        pass

    def tag_layout(self):
        pass

    def ner_layout(self):
        pass

    def seg_action(self, text, **kwargs):
        result = service.segment(text)
        print(result)
        return result


controller = NlpController()
