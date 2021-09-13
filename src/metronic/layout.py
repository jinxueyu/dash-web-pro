import os

from metronic.layouts.menu import build_menu_tag
from metronic.layouts.nav_menu import build_nav_menu
from engine.widgets_manager import Widgets


def build_normal_page(content_container, menu_config):
    widegets = Widgets.instance()

    layout_aside = widegets.get_layout('aside.aside')
    aside_menu = widegets.get_layout('aside.menu')
    aside_brand = widegets.get_layout('aside.brand')
    aside_footer = widegets.get_layout('aside.footer')

    menu = build_menu_tag(menu_config)
    layout_aside = layout_aside(
        aside_menu=aside_menu(menu=menu),
        aside_brand=aside_brand(),
        aside_footer=aside_footer()
    )

    layout_content = widegets.get_layout('content.wrapper')

    content_header = widegets.get_layout('content.header')

    content_footer = widegets.get_layout('content.footer')
    nav_bar = widegets.get_layout('content.navbar')
    top_bar = widegets.get_layout('content.topbar')

    # content
    toolbar_create = widegets.get_widget('content.toolbar_create')
    toolbar_title = widegets.get_widget('content.toolbar_title')
    toolbar_filter = widegets.get_widget('content.toolbar_filter')

    content_toolbar = widegets.get_layout('content.toolbar')
    content_toolbar = content_toolbar(
        toolbar_create=toolbar_create(),
        toolbar_title=toolbar_title(title='Dashboard', sub_title='hello'),
        toolbar_filter=toolbar_filter())

    content_content = widegets.get_layout('content.content')
    content_content = content_content(
        content_toolbar=content_toolbar,
        content_container=content_container
    )

    layout_content = layout_content(
        content_header=content_header(content_navbar=nav_bar(menu=build_nav_menu()), content_topbar=top_bar()),
        content_content=content_content,
        content_footer=content_footer()
    )

    page = widegets.get_layout('page')

    page_layout = page(aside=layout_aside, wrapper=layout_content)

    main_layout = widegets.get_layout('layout')

    return main_layout(page=page_layout)

