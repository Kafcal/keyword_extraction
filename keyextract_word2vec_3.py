# coding=utf-8
import numpy as np
import gensim
import pandas as pd
import jieba.posseg
import codecs
from collections import Counter

model = gensim.models.Word2Vec.load('data/wiki.zh.text.model')


# 此函数计算某词对于模型中各个词的转移概率p(wk|wi)
def predict_proba(oword, iword):
    #获取输入词的词向量
    iword_vec = model[iword]
    #获取保存权重的词的词库
    oword = model.wv.vocab[oword]
    oword_l = model.trainables.syn1[oword.point].T
    dot = np.dot(iword_vec, oword_l)
    lprob = -sum(np.logaddexp(0, -dot) + oword.code*dot)
    return lprob

# 各个词对于某词wi转移概率的乘积即为p(content|wi)，
# 如果p(content|wi)越大就说明在出现wi这个词的条件下，此内容概率越大，
# 那么把所有词的p(content|wi)按照大小降序排列，越靠前的词就越重要，越应该看成是本文的关键词。


def keywords(s, title_keys):
    # 抽出s中和与训练的model重叠的词
    s = [w for w in s if w in model]
    ws = {w: sum([predict_proba(u, w) for u in s]) for w in s}
    # 在标题中的候选词给予一定权重
    for w in s:
        if w in title_keys:
            ws[w] = ws[w] * 0.8
    return Counter(ws).most_common()


def main():
    # 读取数据集
    data_path = 'data/sample_data.csv'
    data = pd.read_csv(data_path)
    ids, titles, contents = data["id"], data["title"], data["content"]
    text_count = len(ids)
    id_list = [ids[k] for k in range(text_count)]
    title_list = [titles[k] for k in range(text_count)]
    content_list = [contents[k] for k in range(text_count)]
    keys = []

    # 定义选取的词性(名词、专有名词、机构团体、地名)
    pos = ['n', 'nz', 'nt', 'ns', 'eng']
    stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]

    # 遍历文件
    for k in range(text_count):
        title = title_list[k]
        content = content_list[k]
        data_ = title + " " + content
        seg = jieba.posseg.cut(data_)  # 分词
        words = []
        for i in seg:
            if i.word not in words and i.word not in stop_key and i.flag in pos:  #去重 + 去停用词 + 词性筛选
                words.append(i.word)

        # 标题分词
        seg_title = jieba.posseg.cut(title)
        title_keys = []
        for i in seg_title:
            if i.word not in title_keys and i.word not in stop_key and i.flag in pos:  #去重 + 去停用词 + 词性筛选
                title_keys.append(i.word)
        x = pd.Series(keywords(words, title_keys))

        # 输出最重要的前10个词
        print(x[0:10])
        keys_ = [x[0:10][i][0] for i in range(10)]
        result = " ".join(keys_)
        keys.append(result)

    # 所有结果写入文件
    result = pd.DataFrame({"id": id_list, "title": title_list, "key": keys}, columns=['id', 'title', 'key'])
    result.to_csv("result/keys_word2vec_new.csv", index=False)


if __name__ == '__main__':
    main()
