#!/usr/bin/python
# coding=utf-8
# 采用Word2Vec词聚类方法抽取关键词1——获取文本词向量表示
import warnings
import codecs
import pandas as pd
import numpy as np
import jieba
import jieba.posseg
import gensim

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')  # 忽略警告


# 返回特征词向量
def get_words_vec(word_list, model):
    name = []
    vec = []
    for word in word_list:
        word = word.replace('\n', '')
        try:
            if word in model:  # 模型中存在该词的向量表示
                name.append(word)
                vec.append(model[word])
        except KeyError:
            continue
    a = pd.DataFrame(name, columns=['word'])
    b = pd.DataFrame(np.array(vec, dtype='float'))
    return pd.concat([a, b], axis=1)


# 数据预处理操作：分词，去停用词，词性筛选
def data_pre(text, stop_key):
    words = []
    pos = ['n', 'nz', 'nt', 'nr', 'ns', 'vn']
    # pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in words and i.word not in stop_key and i.flag in pos:  #去重 + 去停用词 + 词性筛选
            words.append(i.word)
    return words


# 根据数据获取候选关键词词向量
def build_words_vec(data, stop_key, model):
    id_list, title_list, content_list = data['id'], data['title'], data['content']
    for index in range(len(id_list)):
        _id = id_list[index]
        title = title_list[index]
        content = content_list[index]
        l_ti = data_pre(title, stop_key)  # 处理标题
        l_con = data_pre(content, stop_key)  # 处理内容
        # 获取候选关键词的词向量
        words = np.append(l_ti, l_con)  # 拼接数组元素
        words = list(set(words))  # 数组元素去重,得到候选关键词列表
        words_vec = get_words_vec(words, model)  # 获取候选关键词的词向量表示
        # 词向量写入csv文件，每个词400维
        data_vec = pd.DataFrame(words_vec)
        data_vec.to_csv('result/vecs/wordvecs_' + str(_id) + '.csv', index=False)
        print("document ", _id, " well done.")


def main():
    # 读取数据集
    data_file = 'data/sample_data.csv'
    data = pd.read_csv(data_file)
    # 停用词表
    stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]
    # 词向量模型
    inp = 'data/wiki.zh.text.vector'
    model = gensim.models.KeyedVectors.load_word2vec_format(inp, binary=False)
    build_words_vec(data, stop_key, model)


if __name__ == '__main__':
    main()

