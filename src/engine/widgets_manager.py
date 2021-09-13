import os
import threading
import time

from engine import parser
from engine.builder import build_tag, build_checklist_tag
import copy


class Widget(object):
    def __init__(self, widget_config, form_type=None):
        self.config = widget_config
        self.keys = set()
        self.form_type = form_type

    def set_params(self, _config, kwargs):
        for k, v in _config.items():
            if type(v) is dict:
                self.set_params(_config[k], kwargs)

            if type(v) is list:
                for list_v in v:
                    if type(list_v) is dict:
                        self.set_params(list_v, kwargs)

            if type(v) is list:
                for i, list_v in enumerate(v):
                    if type(list_v) is str and list_v.startswith('{{') and list_v.endswith('}}'):
                        prop_name = list_v[2:-2]
                        if prop_name in self.keys:
                            v[i] = kwargs[prop_name]
                        else:
                            v[i] = ''

            if type(v) is str and v.startswith('{{') and v.endswith('}}'):
                prop_name = v[2:-2]
                if prop_name in self.keys:
                    _config[k] = kwargs[prop_name]
                else:
                    _config[k] = ''

    def __call__(self, *args, **kwargs):

        _config = copy.deepcopy(self.config)

        self.keys = set(kwargs.keys())

        self.set_params(_config, kwargs)

        return build_tag(_config, form_type=self.form_type)


class FormWidget(object):
    def __init__(self, widget: Widget, form_action):
        self.__widget = Widget(widget.config, form_type=form_action)

    def __call__(self, *args, **kwargs):
        return self.__widget.__call__(args, kwargs)


def build_widget(widget_config):
    return Widget(widget_config)


def build_form_widget(widget_config):
    return Widget(widget_config, form_type=True)


def read_widget(widget_path):
    with open(widget_path, 'r') as f:
        html = f.read()
        widget_config = parser.parse(html)
        return build_widget(widget_config)


def init_widgets(template_path, widget_path):
    print('widget_path', os.getcwd(), template_path, widget_path)
    widget_dict = {}
    for root, dirs, files in os.walk(template_path+'/'+widget_path):
        # print('////root', root)
        # print('dirs', dirs)
        for file in files:
            if file.endswith('html') or file.endswith('yaml'):
                i = root.find(widget_path)

                widget_name = root[i:].replace('/', '.') + '.' + file.split('.')[0]
                # print('root', widget_name)
            else:
                continue

            widget = read_widget(root + '/' + file)
            widget_dict[widget_name] = widget

    return widget_dict


class Widgets(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        # todo more custom layout
        print('widgets...init....')
        self.init(*args, **kwargs)
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Widgets, "_instance"):
            with Widgets._instance_lock:
                if not hasattr(Widgets, "_instance"):
                    Widgets._instance = Widgets(*args, **kwargs)
        return Widgets._instance

    def init(self, template_path):
        template_paths = None
        if type(template_path) is str:
            template_paths = [template_path]
        else:
            template_paths = template_path

        self.layout_dict = {}
        self.widget_dict = {}
        for p in template_paths:
            layouts_path = 'layouts'
            d = init_widgets(p, layouts_path)
            self.layout_dict.update(d)

            widget_path = 'widgets'
            d = init_widgets(p, widget_path)
            self.widget_dict.update(d)

    def get_input_widget(self, widget_name, control, action, name):
        if widget_name == 'checklist':

            # 'd-flex align-items-center mt-3'
            #     'form-check form-check-inline form-check-solid'
            #         'form-check-input'
            #         'fw-bold ps-2 fs-6'

            config = {
                "tag_name": "checklist",
                "attrs": {
                    'className': 'd-flex align-items-center mt-3',
                    'inputClassName': 'form-check form-check-inline form-check-solid',
                    'labelClassName': 'fw-bold ps-2 fs-6',
                    'labelCheckedClassName': 'labelClassName',
                    'options': [{'label': 'Email', 'value': 1}, {'label': 'Phone', 'value': 2}],
                    'value': [1],
                    'id': {'type': 'action_input', 'control': control, 'action': action, 'name': name}
                }
            }

            return build_checklist_tag(config)

    def get_widget(self, widget_name):
        return self.widget_dict['widgets.'+widget_name]

    def get_form_widget(self, widget_name, control, action):
        return FormWidget(self.widget_dict['widgets.' + widget_name], {'control': control, 'action': action})

    def get_layout(self, layout_name):
        return self.layout_dict['layouts.'+layout_name]


widgets = Widgets.instance('metronic')


def test_dict(d):
    d['name'] = 'hahaha'


if __name__ == '__main__':
    widgets = Widgets('.')
    # widgets = init_widgets('layouts')
    aside = widgets.get_layout('aside.aside')
    print(aside())
    # print(widget(aside=['hello aside!!!']))

    d1 = {'name': 'nuannuan'}

    print(d1['name'])
