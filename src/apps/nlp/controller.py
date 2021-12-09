import dash_echarts

from apps.nlp import layout
from apps.nlp.layout import build_ent_view
from apps.nlp.service import NLPService, pos_tag_name, ner_tag_name, dep_tag_name
from core.controller import Controller

from engine.widgets_manager import Widgets
from metronic.widgets.stretch import build_stretch_card


menu_config = [
    {
        'name': 'NLP',
        'id': 'menu_nlp_100',
        'modules': [
            {
                'name': '语言模型',
                'id': 'menu_nlp_180',
                'icon': 'Home/Library',
                'items': [
                    {
                        'name': '语义表示',
                        'id': 'menu_nlp_181',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'seg_layout'
                    },
                ]

            },
            {
                'name': '词法分析',
                'id': 'menu_nlp_101',
                'icon': 'Text/Font',
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
                        'action': 'pos_layout'
                    },
                    {
                        'name': '命名实体识别',
                        'id': 'menu_nlp_104',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'ner_layout'
                    },
                    {
                        'name': '词向量表示',
                        'id': 'menu_nlp_105',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'ner_layout'
                    },
                    {
                        'name': '词义相似度',
                        'id': 'menu_nlp_106',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'ner_layout'
                    }
                ]
            },
            {
                'name': '句法分析',
                'id': 'menu_nlp_200',
                'icon': 'Text/Article',
                'items': [
                    {
                        'name': '句法依存分析',
                        'id': 'menu_nlp_201',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'dep_layout'
                    },
                    {
                        'name': '文本纠错',
                        'id': 'menu_nlp_202',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'corr_layout'
                    }
                ]
            },
            {
                'name': '文本分析',
                'id': 'menu_nlp_300',
                'icon': 'Files/File',
                'items': [
                    {
                        'name': '关键字提取',
                        'id': 'menu_nlp_301',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'keywords_layout'
                    }, {
                        'name': '文本摘要',
                        'id': 'menu_nlp_302',
                        'icon': 'bullet',
                        'control': 'nlp',
                        'action': 'summary_layout'
                    }
                ]
            }
        ]
    },
    {
        'name': 'Front-End',
        'id': 'menu_fe_100',
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

    service = NLPService()

    def index_layout(self):
        return layout.index(menu_config)

    def seg_layout(self):
        return layout.page('词法分析', '分词', 'seg_action')

    def pos_layout(self):
        return layout.page('词法分析', '词性标注', 'pos_action')

    def ner_layout(self):
        return layout.page('词法分析', '命名实体识别', 'ner_action')

    def dep_layout(self):
        return layout.page('句法分析', '句法依存分析', 'dep_action')

    def corr_layout(self):
        return layout.page('句法分析', '文本纠错', 'correct_action')

    def keywords_layout(self):
        return layout.page('文本分析', '关键字提取', 'keywords_action')

    def summary_layout(self):
        return layout.page('文本分析', '文本摘要', 'summary_action')

    def index_action(self, text):
        doc = self.service.nlp(text)
        head = [
            {'id': 'offset', 'name': 'Offset'},
            {'id': 'word', 'name': '分词'},
            {'id': 'pos_tag', 'name': '词性标注'},
            {'id': 'word_tag', 'name': '词类标注'},
            {'id': 'term_type', 'name': '词类类型'},
            {'id': 'ent_tag', 'name': '实体标注'},
            {'id': 'dep_head', 'name': '依存词'},
            {'id': 'dep_rel', 'name': '依存关系'}
        ]

        for item in doc:
            item['pos_tag'] = pos_tag_name.get(item['pos_tag'])
            # item['word_tag'] =
            item['ner_tag'] = ner_tag_name[item['ner_tag']]
            item['dep_rel'] = dep_tag_name[item['dep_tag']['rel']]
            item['dep_head'] = doc[item['dep_tag']['head'] - 1]['word'] if item['dep_tag']['head'] > 0 else 'Head'

        return layout.build_tasks_view(head, doc)

    def seg_action(self, text, **kwargs):
        result = self.service.seg(text)
        return ', '.join(result)

    def pos_action(self, text, **kwargs):
        outputs = self.service.pos(text)
        return layout.build_ent_view(text, outputs)

    def ner_action(self, text, **kwargs):
        outputs = self.service.ner(text)
        return layout.build_ent_view(text, outputs)

    def dep_action(self, text, **kwargs):
        outputs = self.service.dep(text)
        return layout.build_dep_view(text, outputs)

    def correct_action(self, text, **kwargs):
        correction = self.service.correct(text)
        # offset
        # word
        # tag
        err_len = len(correction)
        output = [''] * err_len

        for i, item in enumerate(correction):
            item['word'] = text[item['offset']: item['offset']+len(item['correction'])]
            item['tag'] = item.pop('correction')
            output[i] = item

        return layout.build_ent_view(text, output)

    def keywords_action(self, text, **kwargs):
        output = self.service.keywords(text)
        return ', '.join([w['word'] for w in output])

    def summary_action(self, text, **kwargs):
        output = self.service.summarize(text)
        return '\n'.join(output)


controller = NlpController()
