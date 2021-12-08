import re

from pyquery import PyQuery as pq


def request_chapter(c_url):
    html = pq(c_url, encoding='utf8')
    d = html('#sonsyuanwen')
    print(d)
    title = d('h1').text()
    arr = re.split('[〔|〕]', d('.source').text())
    author = arr[0]
    niandai = arr[1]
    content = '\n'.join([i.text() for i in d('.contson')('p').items()])

    d = html('#fanyi4163')('.contyishang')
    items = list(d('p').items())

    div_list = list(d('div').items())
    print('div--', div_list)
    if len(div_list) > 1:
        href = div_list[-1]('a').attr('href')

        i = href.find('\'')
        idjm = href[i+1:-1]
        print('==>>>', href, idjm)
        y = pq('https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id='+idjm)
        print(y)
    else:
        yiwen = [i.text() for i in items[1:-1]]
    print(yiwen)


if __name__ == '__main__':
    url = 'https://so.gushiwen.cn/shiwenv_31e46b58b1ff.aspx'
    request_chapter(url)
