import spacy
from spacy import displacy

from LAC import LAC

lac = LAC(mode='lac')
seg = LAC(mode='seg')


def segment(text):
    arr = seg.run([text])
    return ' '.join(arr[0])


if __name__ == '__main__':
    # nlp = spacy.load('en_core_web_m')
    # nlp = spacy.load("zh_core_web_trf")
    # % python -m spacy download zh_core_web_trf
    nlp = spacy.load("/Users/xueyu/Workshop/dash-web-pro/_data/zh_core_web_sm/zh_core_web_sm-3.1.0")
    print(nlp)
    doc = nlp("我爱北京天安门")
    # s = displacy.render(doc, style="dep")
    # print(s)
    displacy.serve(doc, style="dep",
                   options={"compact": True, "bg": "#09a3d5", "color": "white", "font": "Source Sans Pro"})

