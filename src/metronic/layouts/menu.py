from dash import html

from engine.builder import build_tag


def accordion_menu(menu_text, menu_icon, accordion_id, parent_id, children):
    if menu_icon == 'bullet':
        icon = html.Span(className="menu-bullet", children=[html.Span(className="bullet bullet-dot")])
    else:
        icon = html.Span(className="menu-icon", children=[html.I(className="bi bi-" + menu_icon + " fs-2")])

    return html.Div(className="menu-item menu-accordion", id={'type': 'menu-accordion', 'parent': parent_id, 'menu-id': accordion_id},
                    children=[html.Span(className="menu-link", id={'type': 'menu-accordion-button', 'menu-id': accordion_id}, n_clicks=0,
                                        children=[icon,
                                                  html.Span(menu_text, className="menu-title"),
                                                  html.Span(className="menu-arrow")]
                                        ),
                              html.Div(className="menu-sub menu-sub-accordion menu-active-bg", children=children)
                              ]
                    )


def aside_menu_item(menu_type, menu_icon, menu_text, menu_link=None, item_control=None, menu_action=None, children=None, accordion_id=None, parent_id=None):
    if menu_type == 'section':
        return html.Div(className="menu-item",
                        children=[
                            html.Div(className="menu-content pb-2",
                                     children=html.Span(menu_text,
                                                        className="menu-section text-muted text-uppercase fs-8 ls-1"))
                        ])
    elif menu_type == 'accordion':
        return accordion_menu(menu_text, menu_icon, accordion_id, parent_id, children)
    elif menu_type == 'link':
        if menu_icon == 'bullet':
            icon = html.Span(className="menu-bullet", children=[html.Span(className="bullet bullet-dot")])
        else:
            icon = html.Span(className="menu-icon", children=[html.I(className="bi bi-" + menu_icon + " fs-3")])
        return html.Div(className="menu-item",
                        children=[
                            html.A(className="menu-link",
                                   id={'type': 'btn_link', 'control': item_control, 'action': menu_action, 'name': menu_text},
                                   href=menu_link,
                                   children=[icon, html.Span(menu_text, className="menu-title")])]
                        )


aside_menu_config = {
      "tag_name": "div",
      "attrs": {
            "className": [
                  "aside-menu",
                  "flex-column-fluid"
            ]
      },
      "children": [
            {
                  "tag_name": "div",
                  "attrs": {
                        "className": [
                              "hover-scroll-overlay-y",
                              "my-5",
                              "my-lg-5"
                        ],
                        "id": "kt_aside_menu_wrapper",
                        "data-kt-scroll": "true",
                        "data-kt-scroll-activate": "{default: false, lg: true}",
                        "data-kt-scroll-height": "auto",
                        "data-kt-scroll-dependencies": "#kt_aside_logo, #kt_aside_footer",
                        "data-kt-scroll-wrappers": "#kt_aside_menu",
                        "data-kt-scroll-offset": "0"
                  },
                  "children": []
            }
      ]
}

menu_config = {
      "tag_name": "div",
      "attrs": {
            "className": [
                  "menu",
                  "menu-column",
                  "menu-title-gray-800",
                  "menu-state-title-primary",
                  "menu-state-icon-primary",
                  "menu-state-bullet-primary",
                  "menu-arrow-gray-500"
            ],
            "id": "#kt_aside_menu",
            "data-kt-menu": "true"
      },
      "children": []
}


def build_menu_item_tag(item_config, parent_id=None):
    item_name = item_config['name']
    item_id = item_config['id']
    item_icon = item_config['icon']
    item_link = item_config.get('link', '#')
    item_action = item_config.get('action', None)
    item_control = item_config.get('control', None)

    item_children = item_config.get('items', None)
    if item_children is None:
        item_type = 'link'
    else:
        item_type = 'accordion'

    children = []
    if item_children is not None:
        for child in item_children:
            children.append(
                build_menu_item_tag(child, item_id)
            )

    menu_item_tag = aside_menu_item(
        item_type, item_icon, item_name, item_link, item_control, item_action,
        accordion_id=item_id, parent_id=parent_id,
        children=children
    )

    return menu_item_tag


def build_menu_tag(menu):
    menu_item_tags = []
    for group in menu:
        name = group['name']
        menu_item_tags.append(aside_menu_item('section', '', name))
        modules = group['modules']
        id = group['id']

        for module in modules:
            item_tag = build_menu_item_tag(module, id)
            menu_item_tags.append(item_tag)

    return build_tag(menu_config, menu_item_tags)


def build_menu_component():
    menu_tag = build_menu_tag()
    return build_tag(aside_menu_config, [menu_tag])


if __name__ == '__main__':
    build_menu_component()

