from pandas.core.frame import DataFrame
import gensim

model = gensim.models.Word2Vec.load('data/wiki.zh.text.model')

vecs = []
vecs.append(model["足球"])
vecs.append(model["篮球"])

a=[1,2,3,4]#列表a
b=[5,6,7,8]#列表b

c={0 : vecs[0],
   1: vecs[1]}#将列表a，b转换成字典

data=DataFrame(c)#将字典转换成为数据框
print(data.T)