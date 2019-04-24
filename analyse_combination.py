import pandas as pd


result_tfidf = pd.read_csv('result/video_keys_TFIDF.csv')
result_textrank = pd.read_csv('result/video_keys_TextRank.csv')
result_word2vec_bayes = pd.read_csv('result/video_keys_word2vec_bayes.csv')
result_word2vec_cluster = pd.read_csv('result/video_keys_word2vec_cluster.csv')

keys_tfidf = list(result_tfidf["key"])
keys_textrank = list(result_textrank["key"])
keys_word2vec_bayes = list(result_word2vec_bayes["key"])
keys_word2vec_cluster = list(result_word2vec_cluster["key"])

com_tfidf_textrank = []
com_tfidf_bayes = []
com_tfidf_cluster = []
com_textrank_bayes = []
com_textrank_cluster = []
com_bayes_cluster = []

for i in range(len(keys_tfidf)):
    tfidf = keys_tfidf[i].split(" ")
    textrank = keys_textrank[i].split(" ")
    bayes = keys_word2vec_bayes[i].split(" ")
    cluster = keys_word2vec_cluster[i].split(" ")

    com_tfidf_textrank.append(list(set(tfidf).intersection(set(textrank))))
    com_tfidf_bayes.append(list(set(tfidf).intersection(set(bayes))))
    com_tfidf_cluster.append(list(set(tfidf).intersection(set(cluster))))
    com_textrank_bayes.append(list(set(textrank).intersection(set(bayes))))
    com_textrank_cluster.append(list(set(textrank).intersection(set(cluster))))
    com_bayes_cluster.append(list(set(bayes).intersection(set(cluster))))


print("com_tfidf_textrank")
for key in com_tfidf_textrank:
    print(key)

print("com_tfidf_bayes")
for key in com_tfidf_bayes:
    print(key)

print("com_tfidf_cluster")
for key in com_tfidf_cluster:
    print(key)

print("com_textrank_bayes")
for key in com_textrank_bayes:
    print(key)

print("com_textrank_cluster")
for key in com_textrank_cluster:
    print(key)

print("com_bayes_cluster")
for key in com_bayes_cluster:
    print(key)
