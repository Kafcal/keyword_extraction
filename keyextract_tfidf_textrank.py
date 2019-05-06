import jieba.analyse
import numpy as np
import pandas as pd


def softmax(x):
    exp_x = np.exp(x)
    softmax_x = exp_x / np.sum(exp_x)
    return softmax_x


def keyword_extract(title, text_content):
    description = title
    if not description:
        description = title
    jieba.load_userdict('data/newWord.txt')
    jieba.analyse.set_stop_words("data/stopWord.txt")
    # title_keys = jieba.cut(title, cut_all=True)
    # title_keys = [key for key in title_keys]
    title_keys = jieba.lcut(title)
    description_keys = jieba.lcut(description)

    keys_tfidf = jieba.analyse.tfidf(title+" "+description+" "+text_content, topK=20, withWeight=True,
                                     allowPOS=('n', 'nz', 'nt', 'nr', 'ns', 'eng', 'nrt'))
    keys_textrank = jieba.analyse.textrank(title+" "+description+" "+text_content, topK=20, withWeight=True,
                                           allowPOS=('n', 'nz', 'nt', 'nr', 'ns', 'eng', 'nrt'))

    result = []
    for i in range(len(keys_tfidf)):
        flag = 0
        for j in range(len(keys_textrank)):
            if keys_tfidf[i][0] == keys_textrank[j][0]:
                if keys_tfidf[i][0] in title_keys:
                    result.append((keys_tfidf[i][0], (keys_tfidf[i][1] + keys_textrank[j][1]) * 1.2))
                elif keys_tfidf[i][0] in description_keys:
                    result.append((keys_tfidf[i][0], (keys_tfidf[i][1] + keys_textrank[j][1]) * 1.1))
                else:
                    result.append((keys_tfidf[i][0], keys_tfidf[i][1] + keys_textrank[j][1]))
                flag = 1
                break
        if flag == 0:
            if keys_tfidf[i][0] in title_keys:
                result.append((keys_tfidf[i][0], keys_tfidf[i][1] * 1.2))
            elif keys_tfidf[i][0] in description_keys:
                result.append((keys_tfidf[i][0], keys_tfidf[i][1] * 1.1))
            else:
                result.append(keys_tfidf[i])

    result = sorted(result, key=lambda x: -x[1])
    scores = [i[1] for i in result]
    scores = softmax(scores)
    print("-------------------------------------------------", "\n", scores)
    keys = []
    for i in range(10):
        keys.append(result[i][0])
        # if scores[i] >= 0.06:
        #     keys.append(result[i][0])
        # else:
        #     if len(keys) < 3:
        #         keys.append(result[i][0])
        #         keys.append(result[i+1][0])
        #     break

    return keys


def tfidf_textrank(data_path, save_path):
    data = pd.read_csv(data_path)
    ids, titles, contents = list(data["id"]), list(data["title"]), list(data["content"])
    keys = []
    for i in range(len(ids)):
        _keys = " ".join(keyword_extract(titles[i], contents[i]))
        keys.append(_keys)
    result = pd.DataFrame({"id": ids, "title": titles, "key": keys}, columns=['id', 'title', 'key'])
    result.to_csv(save_path, index=False)


tfidf_textrank("data/text_data.csv", "result/keys_tfidf_textrank.csv")
