import json
import time

from dash import html, dcc
import dash_bootstrap_components as dbc

html_tag_set = set(html.__all__)


class DashTag(object):
    def __init__(self, tag_name, attrs, children):
        self.tag_name = tag_name
        self.attrs = attrs
        self.children = children

    def build(self, tag_name, attrs, children=None):
        if 'id' in attrs and type(attrs['id']) is str:
            id_val = attrs['id'].rstrip()
            if len(id_val) > 2 and id_val[0] == '{' and id_val[-1] == '}':
                if id_val.count('"') < 2 <= id_val.count("'"):
                    id_val = id_val.replace("'", '"')
                attrs['id'] = json.loads(id_val)

        has_return = False
        tag_name = tag_name.capitalize()
        if tag_name == 'Input':
            if 'type' in attrs and attrs['type'] != 'text':
                tag = getattr(dbc, 'Input')
            else:
                tag = getattr(dcc, 'Input')

        elif tag_name in html_tag_set:
            tag = getattr(html, tag_name.capitalize())
        else:
            # pass
            print('>>>>>>>>>>>>>', tag_name)

        try:
            return_tag = tag(**attrs, children=children)
        except TypeError:
            print(TypeError, type(tag), tag_name, attrs)
            t = tag()

            keys = list(attrs.keys())
            for k in keys:
                k_in_propnames = k in t._prop_names
                k_in_wildcards = any(
                    k.startswith(w) for w in t._valid_wildcard_attributes
                )

                if not k_in_propnames and not k_in_wildcards:
                    v = attrs.pop(k)
                    print('==>>>>>>>>>>>>==>>>>> pop', k, v)

            return_tag = tag(**attrs, children=children)

        return return_tag

    def tag(self):
        return self.build(self.tag_name, self.attrs,
                          children=None if self.children is None or len(self.children) == 0 else self.children)


def build_form_tag(config, control, action):
    if type(config) is str:
        return config

    # form tag
    if config['tag_name'] == 'form':
        config['attrs']['action'] = '#'

    # button input textarea select
    if config['tag_name'] in ('button', 'input', 'textarea', 'select'):
        input_type = config['attrs'].get('type', None)
        input_name = config['attrs'].get('name', None)
        if input_name is None:
            input_name = time.time()

        if input_type == 'submit':
            config['attrs']['type'] = 'button'
            input_action_type = 'btn_action'
        elif input_type == 'reset':
            input_action_type = 'rest'
        elif input_type == 'checkbox':
            input_action_type = 'action_checkbox'
        else:
            input_action_type = 'action_input'
        config['attrs']['id'] = {'type': input_action_type, 'control': control, 'action': action, 'name': input_name}

    return config


def build_tag(config, children_tag=None, form_type=None):
    if type(config) is str:
        return config

    if form_type is not None:
        config = build_form_tag(config, form_type['control'], form_type['action'])

    if children_tag is None:
        if 'children' in config:
            children_tag = config['children']
        else:
            children_tag = []

    children = []
    if type(children_tag) is list:
        for child in children_tag:
            if type(child) is dict:
                c = build_tag(child, form_type=form_type)
            else:
                c = child
            children.append(c)
    else:
        children.append(children_tag)

    if 'attrs' in config and 'className' in config['attrs']:
        if type(config['attrs']['className']) is list:
            config['attrs']['className'] = ' '.join(config['attrs']['className'])

    return DashTag(config['tag_name'], config['attrs'], children).tag()


def build_checklist_tag(config):
    tag_name = config['tag_name']

    # dbc.Checklist(
    #     options=[
    #         {"label": "Option 1", "value": 1},
    #         {"label": "Option 2", "value": 2},
    #         {"label": "Disabled Option", "value": 3, "disabled": True},
    #     ],
    #     value=[1],
    #     id="checklist-input",
    # )

    attrs = config['attrs']

    return dbc.Checklist(**attrs)
