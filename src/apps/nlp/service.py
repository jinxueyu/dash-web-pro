import json
from functools import reduce
from itertools import accumulate
from pathlib import Path

import spacy
from spacy import displacy

import paddlehub as hub
from paddlenlp.taskflow.knowledge_mining import LABEL_TO_SCHEMA
from paddlenlp.embeddings import TokenEmbedding, list_embedding_name
from paddlenlp import Taskflow
from ddparser import DDParser

import pypinyin

from LAC import LAC

from apps.nlp.summarization import SummaryLACTokenizer, Summarizer, Word2VecInfer

ner_tag_notes = {
    "PERSON": "人，包括虚构",
    "NORP": "民族、宗教或政治团体",
    "FAC": "建筑物、机场、公路、桥梁等",
    "ORG": "公司、中介、事业单位等",
    "GPE": "国家、城市、州",
    "LOC": "地理地点、山脉、水体",
    "PRODUCT": "物品、车辆、食物等(不包括服务)",
    "EVENT": "以飓风、战役、战争、体育赛事等命名",
    "WORK_OF_ART": "书籍、歌曲等",
    "LAW": "制成法律的文件",
    "LANGUAGE": "任意语言",
    "DATE": "绝对或相对的日期或时期",
    "TIME": "比一天短的时间",
    "PERCENT": "百分比，包含%",
    "MONEY": "货币价值，包括单位",
    "QUANTITY": "度量，如重量或距离",
    "ORDINAL": "序数词，如第一第二",
    "CARDINAL": "数量词"
}

tag_to_ent = {
    '人物类_实体': 'PERSON',
    ('人物类_实体', '人物'): 'PERSON',
    ('人物类_实体', '虚拟角色'): 'PERSON',
    ('人物类_实体', '演艺团体'): 'PERSON',
    ('人物类_概念', '人物'): '',
    ('人物类_概念', '虚拟角色'): '',
    ('作品类_实体', '作品与出版物'): 'WORK_OF_ART',
    ('作品类_概念', '作品与出版物'): 'WORK_OF_ART',
    ('作品类_概念', '文化类'): 'WORK_OF_ART',
    '组织机构类': 'ORG',
    ('组织机构类', '组织机构'): 'ORG',
    '组织机构类_企事业单位': 'ORG',
    ('组织机构类_企事业单位', '企事业单位'): 'ORG',
    ('组织机构类_企事业单位', '品牌'): 'ORG',
    ('组织机构类_企事业单位', '组织机构'): 'ORG',
    ('组织机构类_医疗卫生机构', '医疗卫生机构'): 'ORG',
    ('组织机构类_医疗卫生机构', '组织机构'): 'ORG',
    ('组织机构类_国家机关', '国家机关'): 'ORG',
    ('组织机构类_国家机关', '组织机构'): 'ORG',
    ('组织机构类_体育组织机构', '体育组织机构'): 'ORG',
    ('组织机构类_体育组织机构', '组织机构'): 'ORG',
    ('组织机构类_教育组织机构', '教育组织机构'): 'ORG',
    ('组织机构类_教育组织机构', '组织机构'): 'ORG',
    ('组织机构类_军事组织机构', '军事组织机构'): 'ORG',
    ('组织机构类_军事组织机构', '组织机构'): 'ORG',
    ('物体类', '物体与物品'): '',
    ('物体类', '品牌'): '',
    ('物体类', '虚拟物品'): '',
    ('物体类_兵器', '兵器'): '', ('物体类_化学物质', '物体与物品'): '',
    ('物体类_化学物质', '化学术语'): '', ('其他角色类', '角色'): '',
    ('文化类', '文化'): '',
    ('文化类', '作品与出版物'): 'WORK_OF_ART',
    ('文化类', '体育运动项目'): '',
    ('文化类', '语言文字'): 'LANGUAGE',
    ('文化类_语言文字', '语言学术语'): '',
    ('文化类_奖项赛事活动', '奖项赛事活动'): 'EVENT',
    ('文化类_奖项赛事活动', '特殊日'): '',
    ('文化类_奖项赛事活动', '事件'): 'EVENT',
    ('文化类_制度政策协议', '制度政策协议'): 'LAW',
    ('文化类_制度政策协议', '法律法规'): 'LAW',
    ('文化类_姓氏与人名', '姓氏与人名'): '',
    ('生物类', '生物'): '', ('生物类_植物', '植物'): '', ('生物类_植物', '生物'): '', ('生物类_动物', '动物'): '', ('生物类_动物', '生物'): '',
    ('品牌名', '品牌'): '',
    ('品牌名', '企事业单位'): '',
    '场所类': 'LOC',
    ('场所类', '区域场所'): 'LOC',
    ('场所类', '居民服务机构'): 'LOC',
    ('场所类', '医疗卫生机构'): 'LOC',
    ('场所类', '景点'): 'LOC',
    ('场所类_交通场所', '交通场所'): 'LOC',
    ('场所类_交通场所', '设施'): 'FAC',
    ('位置方位', '位置方位'): '',
    '世界地区类': 'GPE',
    ('世界地区类', '世界地区'): 'GPE',
    ('世界地区类', '区域场所'): 'LOC',
    ('世界地区类', '政权朝代'): 'LOC',
    ('饮食类', '饮食'): 'PRODUCT',
    ('饮食类', '生物类'): 'PRODUCT',
    ('饮食类', '药物'): 'PRODUCT',
    ('饮食类_菜品', '饮食'): 'PRODUCT',
    ('饮食类_饮品', '饮食'): 'PRODUCT',
    ('药物类', '药物'): 'PRODUCT',
    ('药物类', '生物类'): 'PRODUCT',
    ('药物类_中药', '药物'): 'PRODUCT',
    ('药物类_中药', '生物类'): 'PRODUCT',
    ('医学术语类', '医药学术语'): '',
    ('术语类_生物体', '生物学术语'): '',
    ('疾病损伤类', '疾病损伤'): '',
    ('疾病损伤类', '动物疾病'): '',
    ('疾病损伤类', '医药学术语'): '',
    ('疾病损伤类_植物病虫害', '植物病虫害'): '',
    ('疾病损伤类_植物病虫害', '医药学术语'): '',
    ('宇宙类', '星体'): '',
    ('宇宙类', '天文学术语'): '',
    '事件类': 'EVENT',
    ('事件类', '事件'): 'EVENT',
    ('事件类', '奖项赛事活动'): 'EVENT',
    '时间类': '',
    ('时间类', '时间阶段'): '-',
    ('时间类', '政权朝代'): 'DATE',
    ('场景事件', '场景事件'): '-',
    '数量词': 'CARDINAL',
    ('数量词', '数量词'): 'CARDINAL',
    ('数量词', '量词'): '-'
}

pos_tag_name = {
    'n': '普通名词', 'f': '方位名词', 's': '处所名词', 'nw': '作品名',
    'nz': '其他专名', 'v': '普通动词', 'vd': '动副词', 'vn': '名动词',
    'a': '形容词', 'ad': '副形词', 'an': '名形词', 'd': '副词',
    'm': '数量词', 'q': '量词', 'r': '代词', 'p': '介词',
    'c': '连词', 'u': '助词', 'xc': '其他虚词', 'w': '标点符号',
    'PER': '人名', 'LOC': '地名', 'ORG': '机构名', 'TIME': '时间'
}

ner_tag_name = {
    "PERSON": "人",
    "NORP": "团体",
    "FAC": "建筑物",
    "ORG": "机构",
    "GPE": "国家、城市、州",
    "LOC": "地点",
    "PRODUCT": "物品",
    "EVENT": "事件",
    "WORK_OF_ART": "艺术作品",
    "LAW": "法律文件",
    "LANGUAGE": "语言",
    "DATE": "日期",
    "TIME": "时间",
    "PERCENT": "百分比",
    "MONEY": "货币",
    "QUANTITY": "度量",
    "ORDINAL": "序数词",
    "CARDINAL": "数量词"
}


dep_tag_name = {
    'SBV': '主谓关系',
    'VOB': '动宾关系',
    'POB': '介宾关系',
    'ADV': '状中关系',
    'CMP': '动补关系',
    'ATT': '定中关系',
    'F': '方位关系',
    'COO': '并列关系',
    'DBL': '兼语结构',
    'DOB': '双宾语结构',
    'VV': '连谓结构',
    'IC': '子句结构',
    'MT': '虚词成分',
    'HED': '核心关系'
}

entity_tag_colors = {
    "ORG": "#7aecec",
    "PRODUCT": "#bfeeb7",
    "GPE": "#feca74",
    "LOC": "#ff9561",
    "PERSON": "#aa9cfc",
    "NORP": "#c887fb",
    "FACILITY": "#9cc9cc",
    "EVENT": "#ffeb80",
    "LAW": "#ff8197",
    "LANGUAGE": "#ff8197",
    "WORK_OF_ART": "#f0d0ff",
    "DATE": "#bfe1d9",
    "TIME": "#bfe1d9",
    "MONEY": "#e4e7d2",
    "QUANTITY": "#e4e7d2",
    "ORDINAL": "#e4e7d2",
    "CARDINAL": "#e4e7d2",
    "PERCENT": "#e4e7d2",
}

pos_tag_colors = {
    'n': '#a370f7', 'f': '#9ec5fe', 's': '#c29ffa', 'nw': '#cfe2ff', 'nz': '#e0cffc',
    'v': '#a98eda', 'vd': '#c5b3e6', 'vn': '#e2d9f3',
    'a': '#e685b5', 'ad': '#efadce', 'an': '#f7d6e6',
    'm': '#e4e7d2', 'q': '#e4e7d2',
    'r': '#0d6efd',
    'd': '#a3cfbb', 'p': '#d1e7dd', 'c': '#79dfc1', 'u': '#a6e9d5', 'xc': '#d2f4ea',
    'w': '#ced4da',
    'PER': '#aa9cfc', 'LOC': '#ff9561', 'ORG': '#7aecec', 'TIME': '#bfe1d9'
}

pos_tag_

class NLPService(object):

    def __init__(self):
        print('...load lac...')

        self.__lac = Taskflow("lexical_analysis")
        # self.__lac = LAC(mode='lac')

        # __ner = Taskflow("ner")
        print('...load tag...')
        self.__word_tag = Taskflow("knowledge_mining", model="wordtag", linking=True)
        # 名词性短语
        # __nptag = Taskflow("knowledge_mining", model="nptag")
        print('...load dep...')
        self.__ddp = DDParser()
        # self.__ddp = Taskflow("dependency_parsing")

        self.__text_correct = Taskflow("text_correction")

        self.__lda_familia_news = hub.Module(name="lda_news")

        self.__token_embedding = TokenEmbedding(embedding_name="w2v.baidu_encyclopedia.target.word-word.dim300")

        self.__summarizer = Summarizer(self.__lac, Word2VecInfer(self.__token_embedding))

    def _lac_tag(self, text):
        outputs = self.__lac(text)
        output = outputs[0]

        # outputs = self.__lac.run([text])
        # output = {
        #     'segs': outputs[0][0],
        #     'tags': outputs[0][1]
        # }

        output.pop('text')
        output['offsets'] = list(accumulate([0] + [len(word) for word in output['segs']][:-1]))
        output['words'] = output.pop('segs')
        output['pos_tags'] = output.pop('tags')
        return output

    def _word_tag(self, text):
        outputs = self.__word_tag(text)
        output = outputs[0]
        return {
            'words': [i['item'] for i in output['items']],
            'word_tags': [i['wordtag_label'] for i in output['items']],
            'term_types': [i['termid'].split('_')[0] if 'termid' in i else '' for i in output['items']],
            'offsets': [i['offset'] for i in output['items']]
        }

    def _basic_tag(self, text):
        # seg pos_tag
        lac_output = self._lac_tag(text)
        # seg word_tag, term_type
        word_output = self._word_tag(text)
        # merge
        return eliminate_differences(text, lac_output, word_output)

    def __nlp_dep(self, input):
        outputs = self.__ddp.parse_seg([input['words']])
        output = outputs[0]

        # input['dep_rels'] = output['deprel']
        # input['dep_heads'] = output['head']

        input['dep_tags'] = [{'head': head, 'rel': rel, 'note': ''} for head, rel in
                             zip(output['head'], output['deprel'])]

        return input

    def __nlp_ner(self, input):
        print('__ner__', input)
        ner_arr = [''] * len(input['words'])
        if 'pos_tags' in input:
            for i, tag in enumerate(input['pos_tags']):
                if tag == 'PER':
                    tag = 'PERSON'
                ner_arr[i] = tag if tag in ner_tag_notes else ''

        if 'term_types' in input and 'word_tags' in input:
            for i, word, word_tag, offset, term_type in zip(range(len(input['words'])), input['words'],
                                                            input['word_tags'], input['offsets'], input['term_types']):
                ent_tag = tag_to_ent.get((word_tag, term_type), '')
                if ent_tag is None or len(ent_tag) <= 1:
                    ent_tag = tag_to_ent.get(word_tag, '')

                if ent_tag is not None and ent_tag in ner_tag_notes:
                    ner_arr[i] = ent_tag

        input['ent_tags'] = ner_arr
        return input

    def __wrap_output(self, output, tag_name):
        return [
            {'offset': offset, 'word': output['words'][i], 'tag': output[tag_name][i]}
            for i, offset in enumerate(output['offsets']) if len(output[tag_name][i]) > 0
        ]

    # 0. 句子分割
    # 1. 词汇标记化 /分词 /seg
    # 2. 预测每个标记的词性/ pos
    # 3. 文本词形还原
    # 4. 识别停止词
    # 5. 依赖解析
    # 6. 寻找名词短语
    # 7. 命名实体识别（NER）
    # 8. 共指解析
    def _nlp(self, text):
        # seg pos_tag, word_tag, term_type
        output = self._basic_tag(text)
        # dep
        output = self.__nlp_dep(output)
        # ner
        output = self.__nlp_ner(output)

        return output

    def nlp(self, text):
        output = self._nlp(text)
        print('_nlp>>>>>>', output)
        return [{
            'offset': output['offsets'][i],
            'word': output['words'][i],
            'pos_tag': output['pos_tags'][i],
            'word_tag': output['word_tags'][i],
            'term_type': output['term_types'][i],
            'dep_tag': output['dep_tags'][i],
            'ent_tag': output['ent_tags'][i]
        } for i, offset in enumerate(output['offsets'])]

    def seg(self, text):
        output = self._basic_tag(text)
        return output['words']

    def pos(self, text):
        output = self._basic_tag(text)
        return self.__wrap_output(output, 'pos_tags')

    def dep(self, text):
        output = self._basic_tag(text)
        output = self.__nlp_dep(output)
        return self.__wrap_output(output, 'dep_tags')

    def ner(self, text):
        output = self._basic_tag(text)
        output = self.__nlp_dep(output)
        output = self.__nlp_ner(output)
        return self.__wrap_output(output, 'ent_tags')

    def ner_mix(self, text, model='mix'):
        # mix lac word
        if model == 'lac' or model == 'mix':
            lac_output = self._lac(text)

        if model == 'word' or model == 'mix':
            word_output = self._word_tag(text)

        ents = self._ner(lac_output, word_output, model=model)

        return [
            {'ent': ents['ents'][i], 'offset': ents['offsets'][i], 'tag': ents['tags'][i]}
            for i in range(len(ents['ents']))
        ]

    def nlp_mix(self, text):

        lac_output = self._lac(text)
        word_output = self._word_tag(text)

        seg_offsets = lac_output['offsets']
        word_offsets = word_output['offsets']

        offsets = list(set(seg_offsets + word_offsets))
        offsets.sort()
        slots_dict = dict([(offset, i) for i, offset in enumerate(offsets)])

        segs = lac_output['words']
        pos_tags = lac_output['tags']
        dep_output = self._dep(segs)
        dep_rels = dep_output['deprel']
        dep_heads = dep_output['head']
        dep_heads = [segs[h - 1] if h > 0 else 'Head' for h in dep_heads]
        ner_output = self._ner_seg(lac_output)
        # ent_tags = self._ner_seg(word_tags)

        word_tags = word_output['tags']
        slots_length = len(slots_dict)

        def fill_slots(offsets, tags):
            slots = [''] * slots_length
            for offset, seg in zip(offsets, tags):
                i = slots_dict[offset]
                slots[i] = seg
            return slots

        segs = fill_slots(seg_offsets, segs)
        pos_tags = fill_slots(seg_offsets, pos_tags)
        dep_rels = fill_slots(seg_offsets, dep_rels)
        dep_heads = fill_slots(seg_offsets, dep_heads)
        ent_tags = fill_slots(ner_output['offsets'], ner_output['tags'])

        word_output = fill_slots(word_offsets, word_output['words'])
        word_tags = fill_slots(word_offsets, word_tags)

        data = [
            {
                'offset': offsets[i],
                'seg': segs[i],
                'pos_tag': pos_tags[i],
                'dep_rel': dep_rels[i],
                'ent_tag': ent_tags[i],
                'word_tag': word_tags[i],
                'dep_head': dep_heads[i],
                'word': word_output[i]
            }
            for i in range(slots_length)
        ]

        return data

    def _correct(self, text):
        correction = self.__text_correct(text)
        # [
        # {'source': '很少有人知道古代中国建筑流璃的烧制中心在山西介休，介休建筑琉璃不仅产量大，而且艺术价值高，工叵们还将烧制技艺传播出去。',
        # 'target': '很少有人知道古代中国建筑琉璃的烧制中心在山西介休，介休建筑琉璃不仅产量大，而且艺术价值高，工具们还将烧制技艺传播出去。',
        # 'errors': [{'position': 12, 'correction': {'流': '琉'}}, {'position': 46, 'correction': {'叵': '具'}}]}
        # ]

        correction = correction[0]
        err_len = len(correction['errors'])
        output = {
            'offsets': [0] * err_len,
            'corrections': [''] * err_len
        }

        for i, e in enumerate(correction['errors']):
            output['offsets'][i] = e['position']
            for c in e['correction'].values():
                output['corrections'][i] += c

        return output

    def correct(self, text):
        correction = self.__text_correct(text)
        correction = correction[0]
        err_len = len(correction['errors'])
        output = [{} for i in range(err_len)]

        for i, e in enumerate(correction['errors']):
            output[i]['offset'] = e['position']
            output[i]['correction'] = ''
            for c in e['correction'].values():
                output[i]['correction'] += c

        return output

    def _lda(self, text):
        # cal_doc_distance(self, doc_text1, doc_text2)
        # cal_doc_keywords_similarity(self, document, top_k=10)
        # cal_query_doc_similarity(self, query, document)
        # infer_doc_topic_distribution(self, document)
        # show_topic_keywords(self, topic_id, k=10)

        doc0 = ''
        doc1 = ''
        self.__lda_news.cal_doc_distance(doc0, doc1)

        q = ''
        doc = ''
        self.__lda_news.cal_query_doc_similarity(q, doc)

    def _lda_doc_keywords(self, text):
        return self.__lda_familia_news.cal_doc_keywords_similarity(text, top_k=100)

    def keywords(self, text):
        keyword_list = self._lda_doc_keywords(text)
        # word_tags = self._basic_tag(text)
        # todo 根据 tag 进行筛选
        return keyword_list

    def _token_embedding(self, word):
        outputs = self.__token_embedding.search(word)
        if outputs is None or len(outputs) == 0:
            return None
        return outputs[0]

    def word_vector(self, word):
        return self._token_embedding(word)

    def summarize(self, text):
        return self.__summarizer.summarize(text)


def make_differences(offset_arr, inputs):
    # for input in inputs:
    #     offset_arr_tmp = [-1] * len(offset_arr)
    #     words = input['words']
    #     offsets = input['offsets']
    #     for offset, w in zip(offsets, words):
    #         word_len = len(w)
    #         if offset_arr_tmp[offset] != offset or offset_arr_tmp[offset + word_len - 1] != offset:
    #             for i in range(offset, offset + word_len):
    #                 if offset_arr_tmp[i] < 0:
    #                     offset_arr_tmp[i] = offset
    #                 else:
    #                     offset_arr_tmp[i] = -1
    #     print(offset_arr_tmp)

    for input in inputs:
        words = input['words']
        offsets = input['offsets']
        for offset, w in zip(offsets, words):
            word_len = len(w)
            offset_code = offset * word_len
            if offset_arr[offset] != offset_code or offset_arr[offset+word_len-1] != offset_code:
                for i in range(offset, offset + word_len):
                    if offset_arr[i] is None:
                        offset_arr[i] = offset_code
                    else:
                        offset_arr[i] = -1
        # print('400>>>>>>>>>', offset_arr)


def eliminate_differences(text, input0, input1):
    output = {}

    item_keys = set([])
    item_keys.update(input0.keys())
    item_keys.update(input1.keys())
    for k in item_keys:
        output[k] = []

    inputs = [input0, input1]
    # print([(i, c) for i, c in enumerate(text)])
    print('input0', input0)
    print('input1', input1)

    # print(input0['words'])
    # print(input0['offsets'])
    # print(input1['words'])
    # print(input1['offsets'])

    offset_arr = [None] * len(text)
    make_differences(offset_arr, inputs)
    print(offset_arr)
    #
    # print([(i, text[i], f) for i, f in enumerate(offset_arr)])
    # print(input0['words'])
    # print(input1['words'])

    input_seqs = [input_to_seq(i) for i in inputs]

    seg_arr = []
    start = 0
    for offset, val in enumerate(offset_arr):
        if offset == 0:
            continue
        if offset_arr[offset - 1] * val < 0:
            seg_arr.append((start, offset, offset_arr[offset - 1]))
            start = offset

    offset = len(offset_arr)
    seg_arr.append((start, offset, offset_arr[offset - 1]))
    if start == 0:
        if val > 0:
            output = {}
            for i in inputs:
                output.update(i)
            return output
        else:
            return mmseg(inputs)

    for start, end, val in seg_arr:
        sub_outputs = [[], []]
        for i, input_seq in enumerate(input_seqs):
            for seq_item in input_seq:
                sub_outputs[i].append(seq_item)
                if seq_item['offsets'] + len(seq_item['words']) >= end:
                    break
        # print(val, start, end, [i['words'] for i in sub_outputs[0]])
        # print(val, [i['words'] for i in sub_outputs[1]])
        # print('>>>>>>>>>>>>>>', start, end, val)
        word_max_len = max([len(s) for s in sub_outputs])
        if val > 0:
            sub_output = [i for i in range(word_max_len)]
            for i in range(word_max_len):
                sub_item = {}
                for sub_out in sub_outputs:
                    for item_key, item_val in sub_out[i].items():
                        if item_val is None:
                            continue
                        if type(item_val) is str and len(item_val) <= 0:
                            continue
                        sub_item[item_key] = item_val
                sub_output[i] = sub_item
        else:
            # mmseg
            sub_output = mmseg(sub_outputs)

        for i, sub_item in enumerate(sub_output):
            for item_key in item_keys:
                output[item_key].append(sub_item.get(item_key, ''))
    return output


def mmseg(inputs):
    # inputs = [
    # [{}],
    # ]
    scores = [0] * len(inputs)
    # 1. 最大匹配
    inputs_words_count = [len(i) for i in inputs]
    # print('inputs_words_count', inputs_words_count)
    for i, count in enumerate(inputs_words_count):
        if count == 1:
            return inputs[i]

    # 2. 最大平均词汇长度
    inputs_words_sum = [sum([len(w['words']) for w in i]) for i in inputs]
    inputs_words_mean = [s*1.0/n for s, n in zip(inputs_words_sum, inputs_words_count)]
    # print('inputs_words_mean', inputs_words_mean)

    max_mean = 0
    max_mean_idx = 0
    pre_mean = inputs_words_mean[0]
    for i in range(1, len(inputs_words_mean)):
        mean = inputs_words_mean[i]
        if mean > max_mean:
            max_mean = mean
            max_mean_idx = i

        if mean != pre_mean:
            pre_mean = -100

    if pre_mean < 0:
        return inputs[max_mean_idx]

    # 3. 最小词长方差
    # (x-xi)**2 / n
    word_len_var = [sum([(len(w['words'])-mean)**2 for w in i])/n for i, mean, n in zip(inputs, inputs_words_mean, inputs_words_count)]

    min_var = 8888
    min_var_idx = 0
    pre_var = word_len_var[0]
    for i in range(1, len(word_len_var)):
        var = word_len_var[i]
        if var < min_var:
            min_var = var
            min_var_idx = i

        if var != pre_var:
            pre_var = -100

    if pre_var < 0:
        return inputs[min_var_idx]

    # print('word_len_var', word_len_var)

    # 4. 最大单字自由度

    return inputs[0]


def input_to_seq(input):
    keys = list(input.keys())
    l = len(input[keys[0]])
    for i in range(l):
        val = {}
        for k in keys:
            val[k] = input[k][i]
        yield val


def run_eliminate_differences():
    case_list = [
        # {
        #     'line': '太阳与太阳系是什么关系',
        #     'input0': {
        #         'words': ['太阳', '与', '太阳系', '是', '什么', '关系'],
        #         'offsets': [0, 2, 3, 6, 7, 9]
        #     },
        #     'input1': {
        #         'words': ['太阳', '与', '太阳系', '是什么关系'],
        #         'offsets': [0, 2, 3, 6]
        #     }
        # }, {
        #     'line': '太阳与太阳系是什么关系,月亮与地球是什么关系？',
        #     'input0': {'offsets': [0, 2, 3, 6, 7, 9, 11, 12, 14, 15, 17, 18, 20, 22],
        #                'words': ['太阳', '与', '太阳系', '是', '什么', '关系', ',', '月亮', '与', '地球', '是', '什么', '关系', '？'],
        #                'pos_tags': ['n', 'p', 'n', 'v', 'r', 'n', 'w', 'n', 'c', 'n', 'v', 'r', 'n', 'w']},
        #     'input1': {'words': ['太阳', '与', '太阳系', '是什么关系', ',', '月亮', '与', '地球', '是什么关系', '？'],
        #                'word_tags': ['宇宙类', '连词', '宇宙类', '疑问词', 'w', '宇宙类', '连词', '宇宙类', '疑问词', 'w'],
        #                'term_types': ['星体', '连词', '天文学术语', '疑问词', '', '星体', '连词', '星体', '疑问词', ''],
        #                'offsets': [0, 2, 3, 6, 11, 12, 14, 15, 17, 22]}
        # }, {
        #     'line': '太阳与太阳系是什么关系,是什么关系？',
        #     'input0': {'offsets': [0, 2, 3, 6, 7, 9, 11, 12, 13, 15, 17],
        #                'words': ['太阳', '与', '太阳系', '是', '什么', '关系', ',', '是', '什么', '关系', '？'],
        #                'pos_tags': ['n', 'p', 'n', 'v', 'r', 'n', 'w', 'v', 'r', 'n', 'w']},
        #     'input1': {'words': ['太阳', '与', '太阳系', '是什么关系', ',', '是什么关系', '？'],
        #                'word_tags': ['宇宙类', '连词', '宇宙类', '疑问词', 'w', '疑问词', 'w'],
        #                'term_types': ['星体', '连词', '天文学术语', '疑问词', '', '疑问词', ''], 'offsets': [0, 2, 3, 6, 11, 12, 17]}
        # }, {
        #     'line': '是什么关系,太阳与太阳系',
        #     'input0': {'offsets': [0, 1, 3, 5, 6, 8, 9], 'words': ['是', '什么', '关系', ',', '太阳', '与', '太阳系'],
        #                'pos_tags': ['v', 'r', 'n', 'w', 'n', 'c', 'n']},
        #     'input1': {'words': ['是什么关系', ',', '太阳', '与', '太阳系'], 'word_tags': ['疑问词', 'w', '宇宙类', '连词', '宇宙类'],
        #                'term_types': ['疑问词', '', '星体', '连词', '天文学术语'], 'offsets': [0, 5, 6, 8, 9]}
        # }, {
        #     'line': "恒泰证券是一家金融公司",
        #     'input0': {'offsets': [0, 4, 5, 7], 'words': ['恒泰证券', '是', '一家', '金融公司'],
        #                'pos_tags': ['ORG', 'v', 'm', 'n']},
        #     'input1': {'words': ['恒泰证券', '是', '一家', '金融公司'], 'word_tags': ['组织机构类_企事业单位', '肯定词', '数量词', '组织机构类_企事业单位'],
        #                'term_types': ['金融组织机构', '肯定否定词', '', '金融组织机构'], 'offsets': [0, 4, 5, 7]}
        # },
        # {
        #     'line': '但无人能够比得上毛泽东',
        #     'input0': {'offsets': [0, 1, 3, 5, 6, 7, 8], 'words': ['但', '无人', '能够', '比', '得', '上', '毛泽东'], 'pos_tags': ['c', 'r', 'v', 'v', 'u', 'v', 'PER']},
        #     'input1': {'offsets': [0, 1, 3, 5, 8], 'words': ['但', '无人', '能够', '比得上', '毛泽东'], 'word_tags': ['连词', '代词', '肯定词', '场景事件', '人物类_实体'], 'term_types': ['连词', '代词', '肯定否定词', '场景事件', '人物']}
        # },
        {
            'line': '前不久，国家电投“暖核一号”在山东海阳市投运',
            'input0': {'offsets': [0, 3, 4, 8, 9, 13, 14, 15, 20], 'words': ['前不久', '，', '国家电投', '“', '暖核一号', '”', '在', '山东海阳市', '投运'], 'pos_tags': ['TIME', 'w', 'n', 'w', 'nz', 'w', 'p', 'ORG', 'v']},
            'input1': {'words': ['前不久', '，', '国家电投', '“', '暖', '核', '一号', '”', '在', '山东', '海阳市', '投运'], 'word_tags': ['时间类', 'w', '组织机构类', 'w', '修饰词', '词汇用语', '数量词', 'w', '介词', '世界地区类', '世界地区类', '场景事件'], 'term_types': ['时间阶段', '', '', '', '修饰词', '', '数量词', '', '介词', '中国地区', '中国地区', '场景事件'], 'offsets': [0, 3, 4, 8, 9, 10, 11, 13, 14, 15, 17, 20]}
        },
        # {
        #     'line': '装机总规模近3000万千瓦',
        #     'input0': {'offsets': [0, 2, 3, 5, 6], 'words': ['装机', '总', '规模', '近', '3000万千瓦'], 'pos_tags': ['vn', 'a', 'n', 'ad', 'm']},
        #     'input1': {'words': ['装机', '总', '规模', '近', '3000万千瓦'], 'word_tags': ['场景事件', '词汇用语', '术语类_符号指标类', '修饰词', '数量词'], 'term_types': ['场景事件', '', '编码符号指标', '场景事件', ''], 'offsets': [0, 2, 3, 5, 6]}
        # }
    ]

    for case in case_list:
        print('line', case['line'])
        output = eliminate_differences(case['line'], case['input0'], case['input1'])
        print(output)
        # print(nlp_ner(output))

    # NLPService.mock_nlp(line, input0, input1)


def run_mmseg():
    case_list = [
        [
            {'words': ['南京市', '长江大桥']},
            {'words': ['南京', '市长', '江大桥']}],
        [
            {'words': ['研究生', '命', '科学']},
            {'words': ['研究', '生命', '科学']}
        ]
    ]
    for inputs in case_list:
        print('-------------------------------------')
        output = mmseg(inputs)
        print('>>>>>', output)


if __name__ == '__main__':
    # nlp = spacy.load('en_core_web_m')
    # nlp = spacy.load("zh_core_web_trf")
    # % python -m spacy download zh_core_web_trf
    # nlp = spacy.load("/Users/xueyu/Workshop/dash-web-pro/_data/zh_core_web_sm/zh_core_web_sm-3.1.0")
    # print(nlp)
    # doc = nlp("我爱北京天安门")
    # # s = displacy.render(doc, style="dep")
    # # print(s)
    # displacy.serve(doc, style="dep",
    #                options={"compact": True, "bg": "#09a3d5", "color": "white", "font": "Source Sans Pro"})

    nlp = None
    # nlp = NLPService()
    texts = [
        # "恒泰证券是一家金融公司",
        # '太阳与太阳系是什么关系,月亮与地球是什么关系？',
        # '太阳与太阳系是什么关系,是什么关系？',
        # '是什么关系,太阳与太阳系',
        # '但无人能够比得上毛泽东',
        '中国共产党的其他领袖人物，每一个都可以同古今中外社会历史上的人物相提并论，但无人能够比得上毛泽东。-- 美国作家史沫特莱'
    ]

    for text in texts:
        if nlp is not None:
            print(text)
            doc = nlp.nlp(text)
            print('nlp', doc)
            # print([(t['word'], t['offset']) for t in doc])
            # doc = nlp.ner(text)
            # print('ner', doc)
            doc = nlp.dep(text)
            # layout.build_dep_view(text, doc)
            print('dep', doc)

    # text = '煤炭、油气之外，还有一批清洁能源“整装待发”、助力能源保供。前不久，国家电投“暖核一号”在山东海阳市投运，核能供暖范围覆盖海阳全城区，惠及20万居民，海阳也成为全国首个“零碳”供暖城市。近期，还有一批大型风电光伏基地项目在内蒙古、甘肃、青海、宁夏等地集中开工，装机总规模近3000万千瓦，比三峡电站的装机容量还大，投产后将为经济社会发展提供更多优质的绿色电力支撑。'
    # output = nlp._word_tag(text)
    # print(output)

    # doc = nlp.ner(line)
    # print(doc)
    # # doc = layout.build_ent_view(line, doc)
    # # print(doc)
    # doc = nlp.nlp(line)
    # print(doc)
    #

    # line = '是什么关系,太阳与太阳系'
    # nlp.nlp(line)
    # print(doc)
    #
    # line = '中国共产党的其他领袖人物，每一个都可以同古今中外社会历史上的人物相提并论，但无人能够比得上毛泽东。-- 美国作家史沫特莱'
    # doc = nlp.nlp(line)
    # print(doc)
    #
    # run_eliminate_differences()

    # run_mmseg()
    text = '很少有人知道古代中国建筑流璃的烧制中心在山西介休，介休建筑琉璃不仅产量大，而且艺术价值高，工叵们还将烧制技艺传播出去。'
    # text_corr = Taskflow("text_correction")
    # t = text_corr(text)
    # print(t)

    lac = LAC(mode='lac')
    doc = lac.run(text)

    print(doc)

    # import pycorrector
    #
    # corrected_sent, detail = pycorrector.correct(text)
    # print(corrected_sent, detail)

    # similarity = Taskflow("text_similarity")

    # lda_news = hub.Module(name="lda_news")
    # jsd, hd = lda_news.cal_doc_distance(doc_text1="今天的天气如何，适合出去游玩吗", doc_text2="感觉今天的天气不错，可以出去玩一玩了")
    # # jsd = 0.003109, hd = 0.0573171
    # print(jsd, hd)
    #
    # lda_sim = lda_news.cal_query_doc_similarity(query='百度搜索引擎',
    #                                             document='百度是全球最大的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，可以瞬间找到相关的搜索结果。')
    # # LDA similarity = 0.06826
    # print(lda_sim)
    #
    # results = lda_news.cal_doc_keywords_similarity('百度是全球最大的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，可以瞬间找到相关的搜索结果。')
    # # [{'word': '百度', 'similarity': 0.12943492762349573},
    # print(results)

    token_embedding = TokenEmbedding(embedding_name="w2v.baidu_encyclopedia.target.word-word.dim300")
