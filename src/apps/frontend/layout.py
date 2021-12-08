from dash import html, dcc

from engine.widgets_manager import Widgets


def layout():
    widgets = Widgets.instance()
    # lay = widgets.get_layout('compact')
    # lay = widgets.get_widget('nlp.card')
    lay = widgets.get_layout('compact')
    return lay()


if __name__ == '__main__':
    widgets = Widgets.instance()
    lay = widgets.get_layout('compact')
    s = lay()

    print(s)
