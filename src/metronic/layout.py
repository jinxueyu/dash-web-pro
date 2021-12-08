
from metronic.layouts.menu import build_menu_tag
from metronic.layouts.nav_menu import build_nav_menu
from engine.widgets_manager import Widgets


def build_normal_page(container, menu_config, title, sub_title):
    widegets = Widgets.instance()
    main_layout = widegets.get_layout('layout')

    # aside
    layout_aside = widegets.get_layout('aside.aside')
    aside_menu = widegets.get_layout('aside.menu')
    aside_brand = widegets.get_layout('aside.brand')
    aside_footer = widegets.get_layout('aside.footer')

    aside_footer = aside_footer()

    menu = build_menu_tag(menu_config)
    layout_aside = layout_aside(
        aside_menu=aside_menu(menu=menu),
        aside_brand=aside_brand(),
        aside_footer=aside_footer
    )

    # wrapper
    wrapper = widegets.get_layout('wrapper.wrapper')
    header = widegets.get_layout('wrapper.header')
    content = widegets.get_layout('wrapper.content')
    footer = widegets.get_layout('wrapper.footer')

    nav_bar = widegets.get_widget('wrapper.header.navbar')
    top_bar = widegets.get_widget('wrapper.header.topbar')

    page_title = widegets.get_widget('wrapper.page_title')
    page_title = page_title(title=title, sub_title=sub_title)

    wrapper = wrapper(
        header=header(navbar=nav_bar(page_title=page_title), topbar=top_bar()),
        content=content(container=container),
        footer=footer()
    )

    return main_layout(aside=layout_aside, wrapper=wrapper)


def build_container(contains):
    widegets = Widgets.instance()
    container = widegets.get_widget('wrapper.container')
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
