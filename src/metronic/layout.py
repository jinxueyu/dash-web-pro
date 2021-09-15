
from metronic.layouts.menu import build_menu_tag
from metronic.layouts.nav_menu import build_nav_menu
from engine.widgets_manager import Widgets


def build_normal_page(contains, content_toolbar, menu_config):
    widegets = Widgets.instance()
    main_layout = widegets.get_layout('layout')

    # aside
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

    # wrapper
    layout_wrapper = widegets.get_layout('wrapper.wrapper')
    wrapper_header = widegets.get_layout('wrapper.header')
    wrapper_content = widegets.get_layout('wrapper.content')
    wrapper_footer = widegets.get_layout('wrapper.footer')

    nav_bar = widegets.get_layout('wrapper.navbar')
    top_bar = widegets.get_layout('wrapper.topbar')

    content_container = build_container(contains)

    layout_wrapper = layout_wrapper(
        content_header=wrapper_header(content_navbar=nav_bar(menu=build_nav_menu()), content_topbar=top_bar()),
        content_content=wrapper_content(content_toolbar=content_toolbar, content_container=content_container),
        content_footer=wrapper_footer()
    )

    return main_layout(aside=layout_aside, wrapper=layout_wrapper)


def build_container(contains):
    widegets = Widgets.instance()
    container = widegets.get_layout('wrapper.container')
    return container(contains=contains)


def build_toolbar(title, sub_title):
    widegets = Widgets.instance()
    toolbar_create = widegets.get_widget('wrapper.toolbar_create')
    toolbar_title = widegets.get_widget('wrapper.toolbar_title')
    toolbar_filter = widegets.get_widget('wrapper.toolbar_filter')
    content_toolbar = widegets.get_layout('wrapper.toolbar')
    content_toolbar = content_toolbar(
        toolbar_create=toolbar_create(),
        toolbar_title=toolbar_title(title=title, sub_title=sub_title),
        toolbar_filter=toolbar_filter())
    return content_toolbar
