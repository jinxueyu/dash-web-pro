import json

from bs4 import BeautifulSoup as soup, NavigableString, Comment

from engine.builder import build_tag

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

    # print('tag_name = ', tag_name)
    # print('attrs = ', attr_dict)
    # print('build_tag(tag_name, attrs)')

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
    doc = soup(text, 'xml')
    tag = doc.contents[0]
    return parse_tag(tag)


def func(**kwargs):
    print(type(kwargs), kwargs)


if __name__ == '__main__':
    html = '''
     <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">
													<path d="M2.56066017,10.6819805 L4.68198052,8.56066017 C5.26776695,7.97487373 6.21751442,7.97487373 6.80330086,8.56066017 L8.9246212,10.6819805 C9.51040764,11.267767 9.51040764,12.2175144 8.9246212,12.8033009 L6.80330086,14.9246212 C6.21751442,15.5104076 5.26776695,15.5104076 4.68198052,14.9246212 L2.56066017,12.8033009 C1.97487373,12.2175144 1.97487373,11.267767 2.56066017,10.6819805 Z M14.5606602,10.6819805 L16.6819805,8.56066017 C17.267767,7.97487373 18.2175144,7.97487373 18.8033009,8.56066017 L20.9246212,10.6819805 C21.5104076,11.267767 21.5104076,12.2175144 20.9246212,12.8033009 L18.8033009,14.9246212 C18.2175144,15.5104076 17.267767,15.5104076 16.6819805,14.9246212 L14.5606602,12.8033009 C13.9748737,12.2175144 13.9748737,11.267767 14.5606602,10.6819805 Z" fill="#000000" opacity="0.3" />
													<path d="M8.56066017,16.6819805 L10.6819805,14.5606602 C11.267767,13.9748737 12.2175144,13.9748737 12.8033009,14.5606602 L14.9246212,16.6819805 C15.5104076,17.267767 15.5104076,18.2175144 14.9246212,18.8033009 L12.8033009,20.9246212 C12.2175144,21.5104076 11.267767,21.5104076 10.6819805,20.9246212 L8.56066017,18.8033009 C7.97487373,18.2175144 7.97487373,17.267767 8.56066017,16.6819805 Z M8.56066017,4.68198052 L10.6819805,2.56066017 C11.267767,1.97487373 12.2175144,1.97487373 12.8033009,2.56066017 L14.9246212,4.68198052 C15.5104076,5.26776695 15.5104076,6.21751442 14.9246212,6.80330086 L12.8033009,8.9246212 C12.2175144,9.51040764 11.267767,9.51040764 10.6819805,8.9246212 L8.56066017,6.80330086 C7.97487373,6.21751442 7.97487373,5.26776695 8.56066017,4.68198052 Z" fill="#000000" />
												</svg>
    '''

    html='''
    <textarea id="{'type': 'action_input', 'control': 'nlp', 'action': '{{action_name}}', 'name': 'text'}" class="form-control form-control-solid" rows="3" name="target_details" placeholder="Type Text">
													中国共产党的其他领袖人物，每一个都可以同古今中外社会历史上的人物相提并论，但无人能够比得上毛泽东。-- 美国作家史沫特莱
													</textarea>
    '''

    code = parse(html)
    print(code)

    # print(code)
    # print(json.dumps(code, indent=4))

    # d = {'k1': 'v1', 'k2': 'v2'}
    # func(k3='v3', k4='v4', **d)
    # id_val = "{'type': 'input_commit', 'control': 'nlp', 'action': 'form_commit', 'index': 2}"
    # val = json.loads(id_val)
    # print(val)

    tag = build_tag(code)

    print(tag)

    from dash import html, dcc
    dcc.Textarea()

