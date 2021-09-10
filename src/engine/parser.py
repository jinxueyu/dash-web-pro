import json

from bs4 import BeautifulSoup as soup, NavigableString, Comment

code_template = '''html.{}({}, 
{}children=[{}])'''


def parser_code(tag_name, attrs, children, deep_len):
    attr_value = []
    for attr in attrs:
        if type(attr) is dict:
            if len(attr) > 0:
                attr_value.append('**' + json.dumps(attr))
        else:
            if type(attr[1]) is list:
                val = ' '.join(attr[1])
            else:
                val = attr[1]
            attr_value.append(attr[0] + '="' + val + '"')

    attrs_value = ', '.join(attr_value)
    children_value = ''
    s = ', \n' + '         '*(deep_len+2)
    if children is not None:
        children_value = s.join(children)

    attr_dict = {}
    for attr in attrs:
        if type(attr) is dict:
            attr_dict.update(attr)
        else:
            if type(attr[1]) is list:
                val = ' '.join(attr[1])
            else:
                val = attr[1]
            attr_dict[attr[0]] = val

    print('tag_name = ', tag_name)
    print('attrs = ', attr_dict)
    print('build_tag(tag_name, attrs)')

    tag_json = {
        'tag_name': tag_name,
        'attrs': attr_dict,
        'children': children
    }

    return code_template.format(tag_name.capitalize(), attrs_value, '         '*(deep_len+1), children_value)


def parse_tag(html_tag):
    if type(html_tag) is Comment:
        return None

    if type(html_tag) is NavigableString:
        print(html_tag)

    attr_dict = {}
    for attr in html_tag.attrs:
        val = html_tag.attrs[attr]

        if attr == 'class':
            attr = 'className'

        if attr == 'autocomplete':
            attr = 'autoComplete'

        if attr == 'autocomplete':
            attr = 'autoComplete'

        if attr == 'accesskey':
            attr = 'accessKey'
            val = val[0]

        if attr == 'style':
            p = False
            if val.startswith('background'):
                p = True
                print('>>>>>', val)
            vals = val.split(';')
            val = {}
            for v in vals:
                style = v.split(':')
                if len(style) > 1:
                    style_key = style[0].strip()
                    if style_key.find('-') > 0:
                        arr = style_key.split('-')
                        style_key = arr[0]
                        for c in range(1, len(arr)):
                            style_key += arr[c].capitalize()
                    val[style_key] = style[1].strip()

            if p:
                print('>>>>>', val)

        attr_dict[attr] = val

    children = []
    for child in html_tag.contents:
        child_tag = None
        if type(child) is NavigableString:
            str_child = child.strip()
            if len(str_child) > 0:
                child_tag = str(str_child)
        else:
            child_tag = parse_tag(child)

        if child_tag is None:
            continue

        children.append(child_tag)

    return {
        'tag_name': html_tag.name,
        'attrs': attr_dict,
        'children': children
    }


def parse(text):
    doc = soup(text, 'lxml')
    tag = doc.body.contents[0]
    return parse_tag(tag)


def func(**kwargs):
    print(type(kwargs), kwargs)


if __name__ == '__main__':
    html = '''
     <div class="card card-xl-stretch mb-xl-8">
        <!--begin::Header-->
        <div class="card-header border-0 pt-5">
            <!--begin::Title-->
            <h3 class="card-title align-items-start flex-column">
                <span class="card-label fw-bolder fs-3 mb-1">Recent Statistics</span>
                <span class="text-muted fw-bold fs-7">More than 400 new members</span>
            </h3>
            <!--end::Title-->
            <!--begin::Toolbar-->
            
            <!--end::Toolbar-->
        </div>
        <!--end::Header-->
        <!--begin::Body-->
        <div class="card-body">
            <!--begin::Chart-->
            <div id='{"id": "kt_charts_widget_1_chart"}' style="height: 350px"></div>
            <!--end::Chart-->
        </div>
        <!--end::Body-->
    </div>
    '''

    code = parse(html)

    # print(code)
    # print(json.dumps(code, indent=4))'

    # d = {'k1': 'v1', 'k2': 'v2'}
    # func(k3='v3', k4='v4', **d)
    id_val = "{'type': 'input_commit', 'control': 'nlp', 'action': 'form_commit', 'index': 2}"
    val = json.loads(id_val)
    print(val)

