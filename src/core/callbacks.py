import json
import dash
from dash import Output, Input, State, ALL, MATCH

from core.app import app

from core.controller import Controllers
from engine.widgets_manager import Widgets


def exec_action_func(control, action, **params):
    print('    exec', control, action)

    controller = Controllers.instance().get(control)
    func = getattr(controller, action)
    return func(**params)


def parse_action(ctx):
    triggered_input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    input_id = json.loads(triggered_input_id)
    control = input_id['control']
    action = input_id['action']

    # for inputs in ctx.inputs_list:
    #     for ipt in inputs:
    #         if 'value' in ipt and ipt['value'] is not None:
    #             action = ipt['id']['action']
    #             control = ipt['id']['control']
    #             break
    #     if control is not None and action is not None:
    #         break

    return control, action


page_route_dict = {
    '/': None,
    '/chat': ('chat', 'layout'),
    '/nlp': {'control': 'nlp', 'action': 'dash_board_page'}
}


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def page_routing(pathname):
    print('fire-->>> page_routing ', pathname)
    if pathname in page_route_dict:
        router = page_route_dict[pathname]
        control = None
        action = None
        if type(router) is tuple or type(router) is list:
            control = router[0]
            action = router[1]
        elif type(router) is dict:
            control = router['control']
            action = router['action']
        else:
            print('routing error')
            return '404'

        return exec_action_func(control, action)
    else:
        return '404'


@app.callback(
    Output('kt_content_container', 'children'),
    Output('toolbar_title', 'children'),
    Input({'type': 'btn_link', 'control': ALL, 'action': ALL, 'name': ALL}, 'n_clicks'),
    State('kt_content_container', 'children'),
    State('toolbar_title', 'children'),
    prevent_initial_call=True
)
def btn_link(n_clicks, state0, state1):
    print('btn_link fire:', n_clicks)
    ctx = dash.callback_context

    print('     ', ctx.triggered, '\n    states_list  ==', ctx.states_list, '\n  states  ==', ctx.states,
          '\n   inputs_list  ', ctx.inputs_list, '\n    inputs  ', ctx.inputs)

    if ctx.triggered[0]['value'] is None:
        print('   >> without bullets <<  ')
        return state0, state1

    control, action = parse_action(ctx)
    if control is None or action is None:
        print('   >> without bullets <<  ')
        return state0, state1

    return exec_action_func(control, action)


def action_callback(n_clicks, states_input):
    result = {'triggered': True}
    ctx = dash.callback_context
    # if ctx.triggered[0]['value'] is None:
    #     print('   >> without bullets <<  ')

    print('    ', ctx.inputs, '\n', ctx.states_list, '\n     ')
    print('    ', states_input)

    if ctx.triggered[0]['value'] is None:
        print('   >> without bullets <<  ')
        result['triggered'] = False
        return result

    control, action = parse_action(ctx)
    if control is None or action is None:
        print('   >> without bullets <<  ')
        result['triggered'] = False
        return result

    req = {}
    for states in ctx.states_list:
        for state in states:
            if 'value' not in state:
                continue

            input_id = state['id']
            input_value = state['value']
            print('   ==>>>> ', type(input_id), input_id, input_value)
            req[input_id['name']] = input_value

    result['result'] = exec_action_func(control, action, **req)
    return result


@app.callback(
    Output({'type': 'action_backdrop',  'control': MATCH, 'action': MATCH, 'name': 0}, 'children'),
    Input({'type': 'btn_action', 'control': MATCH, 'action': MATCH, 'name': ALL}, 'n_clicks'),
    State({'type': 'action_input', 'control': MATCH, 'action': MATCH, 'name': ALL}, 'value'),
    prevent_initial_call=True
)
def btn_action(n_clicks, states_input):
    print('btn_action fire:', n_clicks)
    result = action_callback(n_clicks, states_input)
    if result is None or result['triggered'] is False:
        return None
    print('>>>>>>>>>>>result', result)
    return Widgets.instance().get_widget('common.backdrop')()


@app.callback(
    Output({'type': 'action_box',  'control': MATCH, 'action': MATCH}, 'children'),
    Input({'type': 'btn_action', 'control': MATCH, 'action': MATCH, 'name': ALL}, 'n_clicks'),
    State({'type': 'action_input', 'control': MATCH, 'action': MATCH, 'name': ALL}, 'value'),
    prevent_initial_call=True
)
def btn_interact(n_clicks, states_input):
    print('btn_interact fire:', n_clicks)
    result = action_callback(n_clicks, states_input)
    if result is None or result['triggered'] is False:
        return None
    return result
