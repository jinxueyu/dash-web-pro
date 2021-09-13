from dash import html, dcc
from engine.builder import build_tag

menu_config = {
    "tag_name": "div",
    "attrs": {
        "className": [
            "menu",
            "menu-lg-rounded",
            "menu-column",
            "menu-lg-row",
            "menu-state-bg",
            "menu-title-gray-700",
            "menu-state-title-primary",
            "menu-state-icon-primary",
            "menu-state-bullet-primary",
            "menu-arrow-gray-400",
            "fw-bold",
            "my-5",
            "my-lg-0",
            "align-items-stretch"
        ],
        "id": "#kt_header_menu",
        "data-kt-menu": "true"
    },
    "children": []
}


def header_menu_item(menu_type, menu_icon, menu_text, menu_link=None, children=None, show=False):
    if menu_type == 'accordion':
        if menu_icon == 'bullet':
            icon = html.Span(className="menu-bullet", children=[html.Span(className="bullet bullet-dot")])
        else:
            icon = html.Span(className="menu-icon", children=[html.I(className="bi bi-" + menu_icon + " fs-2")])
        show_menu_class = "menu-item menu-lg-down-accordion me-lg-1"
        if show:
            show_menu_class = "menu-item menu-lg-down-accordion me-lg-1 here show"

        return html.Div(className=show_menu_class, **{'data-kt-menu-trigger': 'click', 'data-kt-menu-placement': "bottom-start"},
                        children=[html.Span(className="menu-link py-3",
                                            children=[icon,
                                                      html.Span(menu_text, className="menu-title"),
                                                      html.Span(className="menu-arrow d-lg-none")]
                                            ),
                                  html.Div(className="menu-sub menu-sub-lg-down-accordion menu-sub-lg-dropdown menu-rounded-0 py-lg-4 w-lg-225px",
                                           children=children)
                                  ]
                        )
    elif menu_type == 'link':
        if menu_icon is None or len(menu_icon) == 0:
            icon = None
            menu_item_class_name = 'menu-item me-lg-1'
        elif menu_icon == 'bullet':
            menu_item_class_name = 'menu-item'
            icon = html.Span(className="menu-bullet", children=[html.Span(className="bullet bullet-dot")])
        else:
            menu_item_class_name = 'menu-item me-lg-1'
            icon = html.Span(className="menu-icon", children=[html.I(className="bi bi-" + menu_icon + " fs-3")])
        # menu-link active py-3
        return html.Div(className=menu_item_class_name,
                        children=[
                            dcc.Link(className="menu-link py-3", href=menu_link,
                                     id={'type': 'link', 'link-id': menu_link},
                                     children=[icon, html.Span(menu_text, className="menu-title")]
                                     )
                        ]
                        )


head_menu = [
    header_menu_item('link', '', 'Dashboard', 'page1'),
    header_menu_item('accordion', '', 'Layouts', 'page2',
                     children=[header_menu_item('link', 'layout-sidebar', 'Aside', 'page3')]
                     )
]


head_menu = [dcc.Link('NLP', href='/nlp'), dcc.Link('Chat', href='/chat')]


def build_nav_menu():
    return build_tag(menu_config, head_menu)
