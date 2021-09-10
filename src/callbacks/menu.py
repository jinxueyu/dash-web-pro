import json
import dash
from dash import Output, Input, State, ALL, MATCH

from core.app import app


@app.callback(
    Output('kt_layout', 'data-kt-aside-minimize'),
    Output('kt_aside', 'className'),
    [Input('kt_aside_toggle', 'n_clicks')],
    [State('kt_aside', 'className'), State('kt_layout', 'data-kt-aside-minimize')],
    prevent_initial_call=True
)
def toggle_aside(input_click, state_class, state_toggle):
    ctx = dash.callback_context
    print('toggle_aside: before trigger:', ctx.triggered, '---', state_class, state_toggle)

    if input_click:
        if state_toggle == 'on':
            state_toggle = 'close'
            # state_class += ' animating'
            # state_class = state_class.replace('aside-hoverable', '')
        else:
            state_toggle = 'on'
            # state_class += ' aside-hoverable'
            # state_class = state_class.replace('animating', '')
        # state_class += ' animating'

    print(' after trigger:', ctx.triggered, '---', state_class, state_toggle)

    return state_toggle, state_class


@app.callback(
    Output({'type': 'menu-accordion', 'parent': ALL, 'menu-id': ALL}, "className"),
    Input({'type': 'menu-accordion-button', 'menu-id': ALL}, "n_clicks"),
    State({'type': 'menu-accordion', 'parent': ALL, 'menu-id': ALL}, "className"),
    prevent_initial_call=True
)
def collapse_menu(n, classNames):
    ctx = dash.callback_context
    triggered_input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    print('collapse_menu: ...', ctx.triggered)

    triggered_value = ctx.triggered[0]["value"]
    if len(triggered_input_id) == 0 or triggered_value is None:
        return [states['value'] for states in ctx.states_list[0]]

    parents_index = [states['id']['parent'] for states in ctx.states_list[0]]

    triggered_input_id = json.loads(triggered_input_id)

    triggered_index = 0
    for inputs in ctx.inputs_list[0]:
        if inputs['id']['menu-id'] == triggered_input_id['menu-id']:
            break
        triggered_index += 1

    states_value = ctx.states_list[0][triggered_index]['value']
    if states_value.find('hover show') >= 0:
        # 关掉自己
        ctx.states_list[0][triggered_index]['value'] = states_value.replace('hover show', '')
        return [states['value'] for states in ctx.states_list[0]]
    else:
        # 关掉所有 除了 parent
        triggered_parent = parents_index[triggered_index]
        for states in ctx.states_list[0]:
            if states['id']['menu-id'] == triggered_parent:
                continue
            states['value'] = states['value'].replace('hover show', '')

        # 打开自己
        ctx.states_list[0][triggered_index]['value'] = states_value.rstrip() + ' hover show'
        return [states['value'] for states in ctx.states_list[0]]