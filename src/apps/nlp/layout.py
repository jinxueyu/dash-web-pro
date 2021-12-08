from apps.nlp.service import pos_tag_colors
from engine import parser
from engine.builder import build_tag
from engine.widgets_manager import Widgets
from metronic.layout import build_normal_page, build_toolbar
from spacy import displacy
import base64
import dash_table as dt

from dash import html, dcc
import dash_bootstrap_components as dbc


def index(menu_config):
    widgets = Widgets.instance()

    contains = widgets.get_widget('nlp.card')

    return build_normal_page(contains(action_name='index_action'), menu_config, 'NLP', 'Hello')


def page(title, sub_title, action_name):
    widgets = Widgets.instance()

    contains = widgets.get_widget('nlp.card')
    page_title = widgets.get_widget('wrapper.page_title')
    page_title = page_title(title=title, sub_title=sub_title)
    return contains(action_name=action_name), page_title


def build_tasks_view(head, data):
    for item in data:
        item['dep_rel'] = item['dep_tag']['rel']
        item['dep_head'] = data[item['dep_tag']['head']-1]['word'] if item['dep_tag']['head'] > 0 else 'Head'

    thead_class = 'fw-bold fs-%d text-gray-800 border-bottom border-gray-200' % len(head)
    table_class = 'table table-hover table-rounded table-striped bg-secondary border gy-%d gs-%d' % (len(data), len(data))

    return build_table_widget(data, head, table_class, thead_class)


def build_table_widget(data, head, table_class, thead_class):
    return dbc.Table([html.Thead(html.Tr([html.Th(c['name']) for c in head]), className=thead_class),
                      html.Tbody([html.Tr([html.Td(row[col['id']]) for col in head]) for row in data])],
                     className=table_class)


def build_ent_view(text, inputs, tag_types=None):
    ents = [{"start": e['offset'], "end": e['offset'] + len(e['word']), "label": e['tag']} for e in inputs]
    doc = {
        "text": text,
        "ents": ents,
        "title": None
    }
    options = {
        'colors': pos_tag_colors
    }
    html = displacy.render(doc, options=options, style="ent", manual=True)
    return build_tag(parser.parse(html))


root_word = {"text": "Root", "tag": "-"}


def build_dep_view(text, input):
    arcs = []
    for i, item in enumerate(input, start=1):
        print('>>>>66<<<<<', i, item)
        head = item['tag']['head']
        label = input[i - 1]['tag']['rel']
        dir, start, end = ('right', head, i) if i > head else ('left', i, head)
        # start, end = (head, i) if dir == 'right' else (i, head)
        arcs.append({
            "start": start,
            "end": end,
            "label": label,
            "dir": dir
        })

    words = [{"text": "Root", "tag": "-"}]
    for i, item in enumerate(input):
        word = item['word']
        words.append({
            'text': word,
            'tag': item['tag']['note']
        })

    dep_src = {
        "words": words,
        "arcs": arcs
    }

    options = {
        'bg': '#09a3d5',
        'color': '#eee',
        'compact': False
    }
    svg = displacy.render(dep_src, style="dep", manual=True, options=options)

    return html.Div(build_tag(parser.parse(svg)), className='scroll-x')

    # return html.Img(src='data:image/svg+xml;base64,'+b64encode(svg))


def b64encode(text):
    text_bytes = text.encode('utf8')
    base64_bytes = base64.b64encode(text_bytes)
    return base64_bytes.decode('utf8')


if __name__ == '__main__':
    import unicodedata
    import chardet
    stringVal = 'abcded'
    print(chardet.detect(str.encode(stringVal)))
    # stringVal = unicodedata.normalize('NFKD', stringVal)
    b = b64encode(stringVal)
    print(b)
