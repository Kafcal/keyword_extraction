# coding=utf-8
import pandas as pd
import jieba.posseg


w1 = '美对华商品将大规模加征关税 我驻美大使：奉陪到底。当地时间22日，美国总统特朗普宣布将对从中国进口的商品大规模征收关税，涉税商品达600亿美元。我驻美大使崔天凯回应：中国从来不想与任何国家进行贸易战，但若其他国家非要对中国施加贸易战，中国一定会予以还击、奉陪到底。'
seg = jieba.posseg.cut(w1)
for i in seg:
    print(i.word, i.flag)

