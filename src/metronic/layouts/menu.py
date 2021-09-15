from dash import html
from dash_svg_component import Svg
from engine.builder import build_tag


def build_icon(icon_name):
    if icon_name == 'bullet':
        return html.Span(className="menu-bullet", children=[html.Span(className="bullet bullet-dot")])

    return html.Span(html.Span(Svg(src='assets/media/icons/duotone/Design/PenAndRuller.svg'),
                               className="svg-icon svg-icon-2"),
                     className="menu-icon")

#                                           <span class="svg-icon svg-icon-2">
# 												<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
# 													<rect x="2" y="2" width="9" height="9" rx="2" fill="black"></rect>
# 													<rect opacity="0.3" x="13" y="2" width="9" height="9" rx="2" fill="black"></rect>
# 													<rect opacity="0.3" x="13" y="13" width="9" height="9" rx="2" fill="black"></rect>
# 													<rect opacity="0.3" x="2" y="13" width="9" height="9" rx="2" fill="black"></rect>
# 												</svg>
# 											</span>


def accordion_menu(menu_text, menu_icon, accordion_id, parent_id, children):
    icon = menu_icon

    return html.Div(
        id={'type': 'menu-accordion', 'parent': parent_id, 'menu-id': accordion_id},
        className="menu-item menu-accordion",
        **{"data-kt-menu-trigger": "click"},
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

    icon = build_icon(menu_icon)

    if menu_type == 'accordion':
        return accordion_menu(menu_text, icon, accordion_id, parent_id, children)

    if menu_type == 'link':
        return html.Div(className="menu-item",
                        children=[
                            html.A(
                                id={'type': 'btn_link', 'control': item_control, 'action': menu_action, 'name': menu_text},
                                className="menu-link",
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

