# import json
#
# import dash
#
# from dash.dependencies import Output, Input, State, MATCH, ALL
#
# from metronic.layout import build_layout, build_page
# from metronic.widgets_manager import Widgets
#
# index_string = """<!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#     </head>
#     <body id="kt_body" class="" style="--kt-toolbar-height:55px;--kt-toolbar-height-tablet-and-mobile:55px" data-kt-scrolltop="on">
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#         <!--begin::Javascript-->
#         <!--begin::Global Javascript Bundle(used by all pages)-->
#
#         <!--end::Global Javascript Bundle-->
#         <!--begin::Page Custom Javascript(used by this page)-->
#
#         <!--end::Page Custom Javascript-->
#         <!--end::Javascript-->
#     </body>
# </html>"""
#
#
# external_stylesheets = ['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700',
#                         'assets/plugins/global/plugins.bundle.css',
#                         'assets/css/style.bundle.css'
#                         ]
# external_scripts = None
# assets_ignore_str = '(css|js)'
#
# app = dash.Dash(__name__,
#                 assets_folder="assets", assets_url_path="assets", assets_ignore=assets_ignore_str,
#                 index_string=index_string,
#                 external_stylesheets=external_stylesheets,
#                 external_scripts=external_scripts)
#
#
# @app.callback(
#     Output('kt_layout', 'data-kt-aside-minimize'),
#     Output('kt_aside', 'className'),
#     [Input('kt_aside_toggle', 'n_clicks')],
#     [State('kt_aside', 'className'), State('kt_layout', 'data-kt-aside-minimize')],
#     prevent_initial_call=True
# )
# def toggle_aside(input_click, state_class, state_toggle):
#     ctx = dash.callback_context
#     print('before trigger:', ctx.triggered, '---', state_class, state_toggle)
#
#     if input_click:
#         if state_toggle == 'on':
#             state_toggle = 'close'
#             # state_class += ' animating'
#             # state_class = state_class.replace('aside-hoverable', '')
#         else:
#             state_toggle = 'on'
#             # state_class += ' aside-hoverable'
#             # state_class = state_class.replace('animating', '')
#         # state_class += ' animating'
#
#     print(' after trigger:', ctx.triggered, '---', state_class, state_toggle)
#
#     return state_toggle, state_class
#
#
# @app.callback(
#     Output({'type': 'menu-accordion', 'parent': ALL, 'menu-id': ALL}, "className"),
#     Input({'type': 'menu-accordion-button', 'menu-id': ALL}, "n_clicks"),
#     State({'type': 'menu-accordion', 'parent': ALL, 'menu-id': ALL}, "className"),
#     prevent_initial_call=True
# )
# def collapse_menu(n, classNames):
#     ctx = dash.callback_context
#     triggered_input_id = ctx.triggered[0]["prop_id"].split(".")[0]
#
#     print('...', ctx.triggered)
#
#     triggered_value = ctx.triggered[0]["value"]
#     if len(triggered_input_id) == 0 or triggered_value is None:
#         return [states['value'] for states in ctx.states_list[0]]
#
#     parents_index = [states['id']['parent'] for states in ctx.states_list[0]]
#
#     triggered_input_id = json.loads(triggered_input_id)
#
#     triggered_index = 0
#     for inputs in ctx.inputs_list[0]:
#         if inputs['id']['menu-id'] == triggered_input_id['menu-id']:
#             break
#         triggered_index += 1
#
#     states_value = ctx.states_list[0][triggered_index]['value']
#     if states_value.find('hover show') >= 0:
#         # 关掉自己
#         ctx.states_list[0][triggered_index]['value'] = states_value.replace('hover show', '')
#         return [states['value'] for states in ctx.states_list[0]]
#     else:
#         # 关掉所有 除了 parent
#         triggered_parent = parents_index[triggered_index]
#         for states in ctx.states_list[0]:
#             if states['id']['menu-id'] == triggered_parent:
#                 continue
#             states['value'] = states['value'].replace('hover show', '')
#
#         # 打开自己
#         ctx.states_list[0][triggered_index]['value'] = states_value.rstrip() + ' hover show'
#         return [states['value'] for states in ctx.states_list[0]]
#
#
# @app.callback(
#     Output('kt_content_container', 'children'),
#     Input({'type': 'menu-button', 'menu-id': ALL}, "n_clicks"),
#     State({'type': 'menu-button', 'menu-id': ALL}, 'className'),
#     State('kt_content_container', 'children'),
#     prevent_initial_call=True
# )
# def menu_click(clicks, states, states_content):
#     ctx = dash.callback_context
#     print('button trigger:', ctx.triggered, '\n', clicks, states, len(states_content))
#     return states_content
#
#
# @app.callback(
#     Output('kt_layout', 'children'),
#     Input('page_url', 'pathname'),
#     prevent_initial_call=True
# )
# def link_action(pathname):
#     ctx = dash.callback_context
#     print('fire===>>>>>', pathname, ctx.triggered)
#     return build_page()
#     # return state
#
# @app.callback(
#     Output('kt_chat_box', 'children'),
#     Output('kt_chat_input_box', 'value'),
#     Input('btn_chat_send', 'n_clicks'),
#     State('kt_chat_box', 'children'),
#     State('kt_chat_input_box', 'value'),
#     State('chat_message_buddy', 'data-message-buddy')
# )
# def State(n_clicks, state_box, state_input, message_buddy_id):
#     if n_clicks:
#         print('fire--', n_clicks, state_box[0], '\n~~~~~', state_input, message_buddy_id)
#         msg_out_widget = Widgets.instance().get_widget('common.chat_message_out')
#         state_box.append(msg_out_widget(message=state_input, message_time_text='Just Now'))
#
#     return state_box[-8:], ''
#
#
# app.layout = build_layout(build_page())
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
