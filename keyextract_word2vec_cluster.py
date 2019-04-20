#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
import math
import jieba.posseg
import codecs
import gensim
from sklearn.cluster import KMeans
from pandas.core.frame import DataFrame


model = gensim.models.Word2Vec.load('data/wiki.zh.text.model')


# 对词向量采用K-means聚类抽取TopK关键词
def get_keywords_kmeans(word_list, top_k, title):
    vecs = []
    for word in word_list:
        vecs.append(model[word])
    vecs_dict = {i: vecs[i] for i in range(len(word_list))}
    vecs = DataFrame(vecs_dict).T

    kmeans = KMeans(n_clusters=1, random_state=10).fit(vecs)
    labels = kmeans.labels_  #类别结果标签
    labels = pd.DataFrame(labels, columns=['label'])
    new_df = pd.concat([labels, vecs], axis=1)
    df_count_type = new_df.groupby('label').size()  #各类别统计个数
    print(df_count_type)
    vec_center = kmeans.cluster_centers_  #聚类中心

    # 定义选取的词性(名词、专有名词、机构团体、地名、英文单词)
    pos = ['n', 'nz', 'nt', 'ns', 'eng', 'nrt']
    stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]
    # 标题分词
    seg_title = jieba.posseg.cut(title)
    title_keys = []
    for i in seg_title:
        if i.word not in title_keys and i.word not in stop_key and i.flag in pos:  #去重 + 去停用词 + 词性筛选
            title_keys.append(i.word)

    # 计算距离（相似性） 采用欧几里得距离（欧式距离）
    distances = []
    vec_words = np.array(vecs)  # 候选关键词向量，dataFrame转array
    vec_center = vec_center[0]  # 第一个类别聚类中心,本例只有一个类别
    length = len(vec_center)  # 向量维度
    for index in range(len(vec_words)):  # 候选关键词个数
        cur_wordvec = vec_words[index]  # 当前词语的词向量
        dis = 0  # 向量距离
        for index2 in range(length):
            dis += (vec_center[index2]-cur_wordvec[index2])*(vec_center[index2]-cur_wordvec[index2])
        dis = math.sqrt(dis)

        # 在文本标题中的词优先
        if word_list[index] in title_keys:
            dis *= 0.5

        distances.append(dis)
    distances = pd.DataFrame(distances, columns=['dis'])

    result = pd.concat([pd.Series(word_list), labels, distances], axis=1)  # 拼接词语与其对应中心点的距离
    result = result.sort_values(by="dis", ascending=True)  # 按照距离大小进行升序排序

    # 抽取排名前topK个词语作为文本关键词
    word_list = np.array(result[0])  # 选择词汇列并转成数组格式
    word_split = [word_list[x] for x in range(0, min(top_k, len(word_list)))]  # 抽取前topK个词汇
    word_split = " ".join(word_split)
    return word_split


def word2vec_cluster(data_path, save_path):
    # 读取数据集
    data = pd.read_csv(data_path)

    ids, titles, contents = data["id"], data["title"], data["content"]
    text_count = len(ids)
    id_list = [ids[k] for k in range(text_count)]
    title_list = [titles[k] for k in range(text_count)]
    content_list = [contents[k] for k in range(text_count)]

    # 定义选取的词性(名词、专有名词、机构团体、地名、英文单词)
    pos = ['n', 'nz', 'nt', 'ns', 'eng', 'nrt']
    stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]

    keys = []
    # 遍历文件
    for i in range(len(id_list)):
        title = title_list[i]
        content = content_list[i]
        data_ = title + " " + content
        seg = jieba.posseg.cut(data_)  # 分词
        words = []
        for k in seg:
            # 去重 + 去停用词 + 词性筛选 + 限制候选词长度
            if k.word not in words and k.word not in stop_key and k.flag in pos and len(k.word) >= 2:
                words.append(k.word)

        words = [w for w in words if w in model]
        article_keys = get_keywords_kmeans(words, 10, title)  # 聚类算法得到当前文件的关键词
        keys.append(article_keys)

    # 所有结果写入文件
    result = pd.DataFrame({"id": id_list, "title": title_list, "key": keys}, columns=['id', 'title', 'key'])
    result = result.sort_values(by="id", ascending=True)  # 排序
    result.to_csv(save_path, index=False)


# def main():
#     # 读取数据集
#     data_path = 'data/text_data.csv'
#     data = pd.read_csv(data_path)
#
#     ids, titles, contents = data["id"], data["title"], data["content"]
#     text_count = len(ids)
#     id_list = [ids[k] for k in range(text_count)]
#     title_list = [titles[k] for k in range(text_count)]
#     content_list = [contents[k] for k in range(text_count)]
#
#     # 定义选取的词性(名词、专有名词、机构团体、地名、英文单词)
#     pos = ['n', 'nz', 'nt', 'ns', 'eng', 'nrt']
#     stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]
#
#     keys = []
#     # 遍历文件
#     for i in range(len(id_list)):
#         title = title_list[i]
#         content = content_list[i]
#         data_ = title + " " + content
#         seg = jieba.posseg.cut(data_)  # 分词
#         words = []
#         for k in seg:
#             # 去重 + 去停用词 + 词性筛选 + 限制候选词长度
#             if k.word not in words and k.word not in stop_key and k.flag in pos and len(k.word) >= 2:
#                 words.append(k.word)
#
#         words = [w for w in words if w in model]
#         article_keys = get_keywords_kmeans(words, 10, title)  # 聚类算法得到当前文件的关键词
#         keys.append(article_keys)
#
#     # 所有结果写入文件
#     result = pd.DataFrame({"id": id_list, "title": title_list, "key": keys}, columns=['id', 'title', 'key'])
#     result = result.sort_values(by="id", ascending=True)  # 排序
#     result.to_csv("result/keys_word2vec_cluster.csv", index=False)
#
#
# if __name__ == '__main__':
#     main()
