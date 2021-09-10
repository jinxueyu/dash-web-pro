from metronic.layout import build_normal_page
from metronic.layouts.grid import build_grid_layout


def container(widgets):
    return build_grid_layout(widgets)


def layout(widgets, menu_config):
    return build_normal_page(container(widgets), menu_config)


print('build dashboard layout.....')
