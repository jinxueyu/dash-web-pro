import json
import dash
from dash import Output, Input, State, ALL

from core.app import app
from engine.widgets_manager import Widgets


@app.callback(
    Output('kt_chat_box', 'children'),
    Output('kt_chat_input_box', 'value'),
    Input('btn_chat_send', 'n_clicks'),
    State('kt_chat_box', 'children'),
    State('kt_chat_input_box', 'value'),
    State('chat_message_buddy', 'data-message-buddy')
)
def State(n_clicks, state_box, state_input, message_buddy_id):
    if n_clicks:
        print('fire--', n_clicks, state_box[0], '\n~~~~~', state_input, message_buddy_id)
        msg_out_widget = Widgets.instance().get_widget('common.chat_message_out')
        state_box.append(msg_out_widget(message=state_input, message_time_text='Just Now'))

    return state_box[-8:], ''
