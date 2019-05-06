# coding=utf-8
import pandas as pd


result_tfidf = pd.read_csv('result/keys_TFIDF.csv')
result_textrank = pd.read_csv('result/keys_TextRank.csv')
result_word2vec_bayes = pd.read_csv('result/keys_word2vec_bayes.csv')
result_word2vec_cluster = pd.read_csv('result/keys_word2vec_cluster.csv')
result_tfidf_textrank = pd.read_csv('result/keys_tfidf_textrank.csv')
result_answer = pd.read_csv('result/keys_reference_answers.csv')

ids, titles = result_answer["id"], result_answer["title"]
text_count = len(ids)
id_list = [ids[k] for k in range(text_count)]
title_list = [titles[k] for k in range(text_count)]
id_list.append(text_count+1)
title_list.append("total")

keys_tfidf = result_tfidf["key"]
keys_textrank = result_textrank["key"]
keys_word2vec_bayes = result_word2vec_bayes["key"]
keys_word2vec_cluster = result_word2vec_cluster["key"]
keys_tfidf_textrank = result_tfidf_textrank["key"]
answer_keys = result_answer["key"]


accuracy_tfidf = []
recall_rate_tfidf = []
accuracy_textrank = []
recall_rate_textrank = []
accuracy_word2vec_bayes = []
recall_rate_word2vec_bayes = []
accuracy_word2vec_cluster = []
recall_rate_word2vec_cluster = []
accuracy_tfidf_textrank = []
recall_rate_tfidf_textrank = []

# 各种算法正确的关键词总数
total_right_cnt_tfidf = 0
total_right_cnt_textrank = 0
total_right_cnt_word2vec_bayes = 0
total_right_cnt_word2vec_cluster = 0
total_right_cnt_tfidf_textrank = 0

# 各种算法关键词总数
total_key_cnt_tfidf = 0
total_key_cnt_textrank = 0
total_key_cnt_word2vec_bayes = 0
total_key_cnt_word2vec_cluster = 0
total_key_cnt_tfidf_textrank = 0

# 答案关键词总数
total_answer_cnt = 0

# 循环处理每一个文本
for i in range(text_count):
    answers = answer_keys[i].split(' ')  # 文本i的参考答案
    list_tfidf = keys_tfidf[i].split(' ')
    list_textrank = keys_textrank[i].split(' ')
    list_word2vec_bayes = keys_word2vec_bayes[i].split(' ')
    list_word2vec_cluster = keys_word2vec_cluster[i].split(' ')
    list_tfidf_textrank = keys_tfidf_textrank[i].split(' ')

    total_key_cnt_tfidf += len(list_tfidf)
    total_key_cnt_textrank += len(list_textrank)
    total_key_cnt_word2vec_bayes += len(list_word2vec_bayes)
    total_key_cnt_word2vec_cluster += len(list_word2vec_cluster)
    total_key_cnt_tfidf_textrank += len(list_tfidf_textrank)

    total_answer_cnt += len(answers)

    right_cnt_tfidf = 0
    right_cnt_textrank = 0
    right_cnt_word2vec_bayes = 0
    right_cnt_word2vec_cluster = 0
    right_cnt_tfidf_textrank = 0

    # tfidf
    for key in list_tfidf:
        if key in answers:
            right_cnt_tfidf += 1
    accuracy_tfidf.append(float(right_cnt_tfidf/len(list_tfidf)))
    recall_rate_tfidf.append(float(right_cnt_tfidf/len(answers)))
    total_right_cnt_tfidf += right_cnt_tfidf

    # textrank
    for key in list_textrank:
        if key in answers:
            right_cnt_textrank += 1
    accuracy_textrank.append(float(right_cnt_textrank/len(list_textrank)))
    recall_rate_textrank.append(float(right_cnt_textrank/len(answers)))
    total_right_cnt_textrank += right_cnt_textrank

    # word2vec_bayes
    for key in list_word2vec_bayes:
        if key in answers:
            right_cnt_word2vec_bayes += 1
    accuracy_word2vec_bayes.append(float(right_cnt_word2vec_bayes/len(list_word2vec_bayes)))
    recall_rate_word2vec_bayes.append(float(right_cnt_word2vec_bayes/len(answers)))
    total_right_cnt_word2vec_bayes += right_cnt_word2vec_bayes

    # word2vec_cluster
    for key in list_word2vec_cluster:
        if key in answers:
            right_cnt_word2vec_cluster += 1
    accuracy_word2vec_cluster.append(float(right_cnt_word2vec_cluster / len(list_word2vec_cluster)))
    recall_rate_word2vec_cluster.append(float(right_cnt_word2vec_cluster / len(answers)))
    total_right_cnt_word2vec_cluster += right_cnt_word2vec_cluster

    # tfidf_textrank
    for key in list_tfidf_textrank:
        if key in answers:
            right_cnt_tfidf_textrank += 1
    accuracy_tfidf_textrank.append(float(right_cnt_tfidf_textrank / len(list_tfidf_textrank)))
    recall_rate_tfidf_textrank.append(float(right_cnt_tfidf_textrank / len(answers)))
    total_right_cnt_tfidf_textrank += right_cnt_tfidf_textrank

# 统计总的准确率
accuracy_tfidf.append(float(total_right_cnt_tfidf/total_key_cnt_tfidf))
accuracy_textrank.append(float(total_right_cnt_textrank/total_key_cnt_textrank))
accuracy_word2vec_bayes.append(float(total_right_cnt_word2vec_bayes/total_key_cnt_word2vec_bayes))
accuracy_word2vec_cluster.append(float(total_right_cnt_word2vec_cluster/total_key_cnt_word2vec_cluster))
accuracy_tfidf_textrank.append(float(total_right_cnt_tfidf_textrank/total_key_cnt_tfidf_textrank))

# 统计总的召回率
recall_rate_tfidf.append(float(total_right_cnt_tfidf/total_answer_cnt))
recall_rate_textrank.append(float(total_right_cnt_textrank/total_answer_cnt))
recall_rate_word2vec_bayes.append(float(total_right_cnt_word2vec_bayes/total_answer_cnt))
recall_rate_word2vec_cluster.append(float(total_right_cnt_word2vec_cluster/total_answer_cnt))
recall_rate_tfidf_textrank.append(float(total_right_cnt_tfidf_textrank/total_answer_cnt))

# 分析结果写入文件
result1 = pd.DataFrame({"id": id_list, "title": title_list, "accuracy": accuracy_tfidf, "recall_rate": recall_rate_tfidf},
                       columns=['id', 'title', 'accuracy', 'recall_rate'])
result1.to_csv("result/analyse_tfidf.csv", index=False)


result1 = pd.DataFrame({"id": id_list, "title": title_list, "accuracy": accuracy_textrank,
                        "recall_rate": recall_rate_textrank}, columns=['id', 'title', 'accuracy', 'recall_rate'])
result1.to_csv("result/analyse_textrank.csv", index=False)


result1 = pd.DataFrame({"id": id_list, "title": title_list, "accuracy": accuracy_word2vec_bayes,
                        "recall_rate": recall_rate_word2vec_bayes},
                       columns=['id', 'title', 'accuracy', 'recall_rate'])
result1.to_csv("result/analyse_word2vec_bayes.csv", index=False)


result1 = pd.DataFrame({"id": id_list, "title": title_list, "accuracy": accuracy_word2vec_cluster,
                        "recall_rate": recall_rate_word2vec_cluster},
                       columns=['id', 'title', 'accuracy', 'recall_rate'])
result1.to_csv("result/analyse_word2vec_cluster.csv", index=False)


result1 = pd.DataFrame({"id": id_list, "title": title_list, "accuracy": accuracy_tfidf_textrank,
                        "recall_rate": recall_rate_tfidf_textrank},
                       columns=['id', 'title', 'accuracy', 'recall_rate'])
result1.to_csv("result/analyse_tfidf_textrank.csv", index=False)


print("tfidf", "标注数量:", total_key_cnt_tfidf, "正确数量:", total_right_cnt_tfidf, "答案数量", total_answer_cnt)
print("textrank", "标注数量:", total_key_cnt_textrank, "正确数量:", total_right_cnt_textrank, "答案数量", total_answer_cnt)
print("word2vec_bayes", "标注数量:", total_key_cnt_word2vec_bayes, "正确数量:", total_right_cnt_word2vec_bayes, "答案数量", total_answer_cnt)
print("word2vec_cluster", "标注数量:", total_key_cnt_word2vec_cluster, "正确数量:", total_right_cnt_word2vec_cluster, "答案数量", total_answer_cnt)
print("tfidf_textrank", "标注数量:", total_key_cnt_tfidf_textrank, "正确数量:", total_right_cnt_tfidf_textrank, "答案数量", total_answer_cnt)
