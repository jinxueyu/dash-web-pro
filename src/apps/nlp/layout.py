
from engine.widgets_manager import Widgets
from metronic.layout import build_normal_page, build_toolbar


def index(menu_config):
    widgets = Widgets.instance()

    contains = widgets.get_widget('nlp.card')

    toolbar = build_toolbar(title='Hello', sub_title='Nlp')

    return build_normal_page(contains(), toolbar, menu_config)
