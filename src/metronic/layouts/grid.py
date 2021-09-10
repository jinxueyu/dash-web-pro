from engine.builder import build_tag

kt_content_container_config = {
    'tag_name': 'div',
    'attrs': {
    }
}


def build_grid_layout(widgets):
    row_tag_config = {
            'tag_name': 'div',
            'attrs': {
                'className': 'row g-5 g-xl-8'.split()
            }
    }

    col_tag_config = {
        'tag_name': 'div',
        'attrs': {
            'className': []
        }
    }

    rows = []
    for widgets_of_row in widgets:
        row_children_tag = []
        col_3_class_name = ['col-xl-4']
        col_2_class_name = ['col-xl-6']

        row_length = len(widgets_of_row)

        if row_length == 3:
            col_tag_config['attrs']['className'] = col_3_class_name
        elif row_length == 2:
            col_tag_config['attrs']['className'] = col_2_class_name

        for widget_col in widgets_of_row:
            if type(widget_col) is list:
                col_children = widget_col
            else:
                col_children = [widget_col]

            row_children_tag.append(build_tag(col_tag_config, col_children))

        rows.append(build_tag(row_tag_config, row_children_tag))

    return build_tag(kt_content_container_config, rows)

