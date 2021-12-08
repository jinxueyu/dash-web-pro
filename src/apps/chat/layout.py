from engine.widgets_manager import Widgets
from metronic.layout import build_normal_page


def build_chat_private():
    chat_widget = Widgets.instance().get_widget('common.chat_private')
    return chat_widget()

menu_config = [
        {
            'name': 'Dashboard',
            'id': 1,
            'modules': [
                {
                    'name': 'chat',
                    'id': 'seg',
                    'control': 'chat',
                    'action': 'dashboard',
                    'icon': 'app-indicator'
                }
            ]
        }
]

toolbar_title = Widgets.instance().get_widget('wrapper.toolbar_title')

layout = build_normal_page(build_chat_private(), menu_config, '', '')
