
import dash_ace

from engine.widgets_manager import Widgets
from metronic.layout import build_normal_page
from metronic.layouts.grid import build_grid_layout


def container(widgets):
    return build_grid_layout(widgets)


def layout(widgets, menu_config):
    return build_normal_page(container(widgets), menu_config)


def account_basic_info():
    toolbar_title = Widgets.instance().get_widget('content.toolbar_title')

    checklist = Widgets.instance().get_input_widget('checklist', 'nlp', 'action', 'communication')

    info_page = Widgets.instance().get_widget('nlp.account_basic_info')

    return info_page(checklist_communication=checklist), toolbar_title(title='Hello', sub_title='basic')


def ide_layout(result):
    widegets = Widgets.instance()
    webide = widegets.get_widget('nlp.webide')

    toolbar_title = Widgets.instance().get_widget('content.toolbar_title')
    ide_widget = dash_ace.DashAceEditor(
        id={"type": "action_input", "control": "nlp", "action": "ide_commit", "name": "code"},
        value='def test(a: int) -> str : \n'
              '    return f"value is {a}"',
        theme='monokai',
        mode='python',
        tabSize=4,
        enableBasicAutocompletion=True,
        enableLiveAutocompletion=True,
        placeholder='Python code ...',
        width='640px',
        height='280px'
    )
    return webide(ide_widget=ide_widget, result=result), toolbar_title(title='Hello', sub_title='IDE')


print('build dashboard layout.....')
