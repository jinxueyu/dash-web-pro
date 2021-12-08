import logging
import os
import re
import numpy as np
from LAC import LAC

from gensim.summarization.summarizer import _extract_important_sentences as extract_important_sentences
from gensim.summarization import summarize_corpus
from paddlenlp import Taskflow
from paddlenlp.embeddings import TokenEmbedding

logger = logging.getLogger(__name__)

RE_SENTENCE = re.compile(r'(\S.+?[.!?])(?=\s+|$)|(\S.+?[。！？])(?=[\S\s]+|$)|(\S.+?)(?=[\n]|$)', re.UNICODE)


def split_sentences(text):
    for match in RE_SENTENCE.finditer(text):
        yield match.group()


def load_config(config_file, config=None):
    """
    Args:
        config_file: model configuration file.
        config: ModelConfig class
    """
    if config is None:
        config = ModelConfig()

    logger.info("Loading LDA config.")
    with open(config_file, 'r', encoding='utf-8') as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
        config.__dict__.update(yaml_dict)

    return config


class Sentence(object):
    def __init__(self, text, tokens, index):
        self.index = index
        self.text = text
        self.tokens = tokens


class SummaryModel(object):
    def __init__(self, ratio=0.2, word_count=None, split=False):
        self.ratio = ratio
        self.word_count = word_count
        self.split = split

    def summarize(self, corpus):
        most_important_docs = summarize_corpus(corpus, ratio=self.ratio if self.word_count is None else 1)
        return most_important_docs


class WordVector(object):
    def __init__(self, token_embedding):
        self.__token_embedding = token_embedding

    def vector(self, words):
        return self.__token_embedding.search(words)


class InferenceEngine(object):
    def __init__(self, vector_infer):
        # ratio = 0.2, word_count = None, split = False
        self.__model = SummaryModel(ratio=0.2, word_count=None, split=False)
        self.__word_vector = vector_infer

    def build_corpus(self, sentences):
        """Construct corpus from provided sentences.

        Parameters
        ----------
        sentences : list of :class:`~gensim.summarization.syntactic_unit.SyntacticUnit`
            Given sentences.

        Returns
        -------
        list of list of (int, int)
            Corpus built from sentences.
        """

        def corpus(tokens):
            if len(tokens) == 0:
                return []
            cp = self.__word_vector.infer(tokens)
            if cp is None:
                return np.zeros((self.__word_vector.dim()))
            return cp

        return [corpus(sent.tokens) for sent in sentences]

    def infer(self, sentences):
        if len(sentences) == 0:
            logger.warning("Input text is empty.")
            return [] if self.__model.split else u""

        # If only one sentence is present, the function raises an error (Avoids ZeroDivisionError).
        if len(sentences) == 1:
            raise ValueError("input must have more than one sentence")

        # Warns if the text is too short.
        INPUT_MIN_LENGTH = 4
        if len(sentences) < INPUT_MIN_LENGTH:
            logger.warning("Input text is expected to have at least %d sentences.", INPUT_MIN_LENGTH)

        corpus = self.build_corpus(sentences)
        most_important_docs = self.__model.summarize(corpus)

        if not most_important_docs:
            logger.warning("Couldn't get relevant sentences.")
            return [] if self.__model.split else u""

        extracted_sentences = extract_important_sentences(sentences, corpus, most_important_docs, self.__model.word_count)

        # Sorts the extracted sentences by apparition order in the original text.
        extracted_sentences.sort(key=lambda s: s.index)
        return [sent.text for sent in extracted_sentences]


class Tokenizer(object):
    """Base tokenizer class.
    """

    def __init__(self):
        pass

    def tokenize(self, text):
        raise NotImplementedError


class SummaryLACTokenizer(Tokenizer):

    def __init__(self, lac, vocab_path=None):
        super().__init__()
        self.__max_word_len = 0
        self.__vocab = set()
        self.__lac = lac
        if vocab_path is not None:
            self.__load_vocab(vocab_path)

    def __load_vocab(self, vocab_path):
        """Load the word dictionary.
                """
        with open(vocab_path, 'r', encoding='utf-8') as fin:
            vocab_size = 0
            for line in fin.readlines():
                fields = line.strip().split('\t')
                assert len(fields) >= 2
                word = fields[1]
                self.__max_word_len = max(self.__max_word_len, len(word))
                self.__vocab.add(word)
                vocab_size += 1

    def tokenize(self, text):
        sentences = split_sentences(text)
        units = []
        i = 0
        for s in sentences:
            print('Sentence', s)
            units.append(Sentence(s, self.tok(s), i))
            i += 1
        return units

    def tok(self, text):
        # results = self.__lac.run(text)
        results = self.__lac(text)
        words = results[0]['segs']
        pos_tags = results[0]['tags']

        output = []
        for i in range(0, len(words)):
            word = words[i]
            l = pos_tags[i]
            if len(word.rstrip()) < 2:
                continue
            if l in ('w', 'u', 'c', 'p', 'd', 'xc'):
                continue
            output.append(word)
        return output

    def contains(self, word):
        """Check whether the word is in the vocabulary.
        """
        return word in self.__vocab


class Word2VecInfer(object):
    def __init__(self, token_embedding):

        self.__model = token_embedding

    def dim(self):
        return self.__model.embedding_dim

    def infer(self, tokens):
        if tokens is None or len(tokens) == 0:
            return None

        v1 = []
        for word in tokens:
            vec = self.__model.search(word)
            if vec is not None:
                v1.append(vec[0])

        if len(v1) == 0:
            return None

        return np.array(v1).mean(axis=0)


class Summarizer(object):

    def __init__(self, lac, vector):
        self.__tokenizer = SummaryLACTokenizer(lac)
        self.__infer = InferenceEngine(vector)

    def summarize(self, text):
        text_tokens = self.__tokenizer.tokenize(text)
        return self.__infer.infer(text_tokens)


if __name__ == '__main__':
    text = '''
  全数据分析，具备国际竞争力的中国座舱电子龙头。
    简介：脱胎于德系T1豪门，专注座舱电子领域近三十年
    公司主要产品为多媒体娱乐（收音机等）和导航车机，两者合计2016年收入占比达到85%。公司客户优质，前五大客户为通用五菱、一汽大众、长城汽车等。
    公司由西门子汽车电子事业部重组而来，自90年代初即拥有了自主产品研发能力。
    受益于下游自主品牌放量和新客户导入，过去四年收入复合增速超过45%，2016年收入超过50亿元，净利润约6亿元。
    上市：募投后产能预计翻倍，中国汽车电子产业崛起的起点汽车电子包括座舱电子、车身电子、控制系统三部分。
    我们预计公司在自主座舱电子市场份额超过30%且客户优质。座舱电子有望首先实现国产化但2016年国产化率我们预计仍不到20%。
    公司此次IPO募集资金净额约20亿元扩张产能投向ADAS（毫米波雷达）、智能驾驶舱（导航车机）等方向，同时补充流动资金。达产后我们预计总产能实现翻倍。
    空间：战略思维超前，公司成长天花板远未到来
    与海外座舱电子龙头哈曼相比，公司收入规模仅为哈曼约六分之一。公司成长驱动因素之一为国产化，即进入合资体系和国际化。
    公司较早布局海外，2012~2013年即在德国和日本设立子公司，此前已经获得德系和日系标杆案例。受益新客户落地，公司未来五年市场份额有望加速提升。
    公司成长驱动因素之二为单价提升，即ADAS、智能驾驶舱量产。我们预计公司ADAS（毫米波雷达）预计未来三年有望占据公司三分之一收入。
    IPO募投后产能翻倍，我们看好公司未来三年保持较快增长态势。
    竞争力：出身德系豪门，全数据分析中国座舱电子龙头核心能力我们认为，公司座舱电子自主研发能力国内排名遥遥领先。
    维度之一，外资T1研发体系传承和三十年的积累。
    公司自成立伊始便师承西门子研发体系，相比国内同行，无论是在时间积累还是在外资T1体系角色有显著优势维度之二，重视产品创新，研发投入遥遥领先。
    公司一直重视研发，在研发投入的金额上同行业绝对额排名第一，相对额（比例）排名前列。而在研发投入成果上，公司在智能驾驶舱虚拟化技术、ADAS毫米波雷达技术等前瞻研发覆盖全面性第一。
    维度之三，员工激励充分。尽管是一家国企，但是员工持股比例高达24%，同时激励覆盖全面占研发人员约16%。
    首次覆盖给予增持评级，看好公司加速进入全球座舱电子产业链公司是为数不多具备国际竞争力的座舱电子厂商。新客户和新产品2019年加速导入，预计2017-2019年EPS分别为1.09、1.22、1.66元。
    考虑竞争力结合行业平均估值，我们给予目标价40元，对应2018年33X。
    风险提示：产品价格下降风险、全球顶级车厂审厂周期低于预期、毫米波雷达等ADAS产品放量低于预期。
    '''

    sentences = split_sentences(text)
    print(list(sentences))

    lac = Taskflow("lexical_analysis")
    token_embedding = TokenEmbedding(embedding_name="w2v.baidu_encyclopedia.target.word-word.dim300")
    wv = Word2VecInfer(token_embedding)
    summarizer = Summarizer(lac, wv)

    lines = summarizer.summarize(text)
    for line in lines:
        print(line)
