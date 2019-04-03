import numpy as np
import gensim
model = gensim.models.Word2Vec.load('data/wiki.zh.text.model')


#此函数计算某词对于模型中各个词的转移概率p(wk|wi)
def predict_proba(oword, iword):
    #获取输入词的词向量
    iword_vec = model[iword]
    #获取保存权重的词的词库
    oword = model.wv.vocab[oword]
    oword_l = model.trainables.syn1[oword.point].T
    dot = np.dot(iword_vec, oword_l)
    lprob = -sum(np.logaddexp(0, -dot) + oword.code*dot)
    return lprob

#各个词对于某词wi转移概率的乘积即为p(content|wi)，
#如果p(content|wi)越大就说明在出现wi这个词的条件下，此内容概率越大，
#那么把所有词的p(content|wi)按照大小降序排列，越靠前的词就越重要，越应该看成是本文的关键词。


from collections import Counter
def keywords(s):
    #抽出s中和与训练的model重叠的词
    s = [w for w in s if w in model]
    ws = {w:sum([predict_proba(u, w) for u in s]) for w in s}
    return Counter(ws).most_common()


import pandas as pd
import jieba
#这里我们随便去弄一篇微博
#之前说过使用word2vec不需要去除停用词

w1 = u'美对华商品将大规模加征关税 我驻美大使：奉陪到底。当地时间22日，美国总统特朗普宣布将对从中国进口的商品大规模征收关税，涉税商品达600亿美元。我驻美大使崔天凯回应：中国从来不想与任何国家进行贸易战，但若其他国家非要对中国施加贸易战，中国一定会予以还击、奉陪到底。'
x = pd.Series(keywords(jieba.cut(w1)))
#输出最重要的前13个词
print (x[0:13])
