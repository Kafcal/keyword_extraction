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


def keywords(s):
    # 抽出s中和与训练的model重叠的词,去停用词
    s = [w for w in s if w in model]
    ws = {w: sum([predict_proba(u, w) for u in s]) for w in s}
    return Counter(ws).most_common()


w1 = '美对华商品将大规模加征关税 我驻美大使：奉陪到底。当地时间22日，美国总统特朗普宣布将对从中国进口的商品大规模征收关税，涉税商品达600亿美元。我驻美大使崔天凯回应：中国从来不想与任何国家进行贸易战，但若其他国家非要对中国施加贸易战，中国一定会予以还击、奉陪到底。'
w2 = u'你可以在微博微信喜马拉雅b站等平台找到我们，请问你觉得这个视频难做吗什么都做之前我不知道为什么我会认识繁体字丹肠道感觉也还行就，就算这句话中可能有你不熟悉的繁体字你只要读出其中所有的传承字然后再根据上下文语境就能自动地不熟悉的繁体字翻译过来，你好能顺畅的读书这段话因为你已经识别出这一段歌词及时你的老师从来没教过你这些字应该怎么读，其实都是繁体字幕三简体汉字同根同源高度相似的字形结构以及大量传承字的存在是繁简转换器存在的外部因素而人脑匪夷所思的信息重建能力就是反向转换器存在的内部因素，比如大部分人在阅读的时候都采取了整体阅读的方式无论一段文字中掺杂的繁体字yy文字或者干脆脱掉这些文字都不会影响信息的获取而改变文字顺序或者大小也不会影响正常阅读，2013年正式颁布的通用规范汉字表一共收入了8105个汉字其中有2546个左右的汉字是由繁体字简化得到的简体字，还有一大批汉字只保留了猿繁体字中的一部分另外还有一批轮廓子也就是保留的袁繁体字的轮廓特征值的具体的笔画进行简化，从字形结构上看绝大多数简体字都保留的原繁体字中最重要的形态特征上过学的中国人联盟太太就有很高的正确率除了简体字以外通用规范汉字表中有超过三分之二的汉字都是传承字也就是历史上留存下来并且在各地沿用至今的汉字它们既不属于繁体字也不属于简体字还是各类汉字系统中的共同组成部分是连接繁简字之间的桥梁，1956年1月31日人民日报全文发表了国务院制定的汉字简化方案公布了第一批简化汉字其中一大批文字的字形结构梅便只是把繁体字中比较复杂的部分改成了简单的符号，永远不要低估大脑的信息进口能力别说繁体字就连阅读根本不存在的火星文都不是什么难事趁着同学阅读好几种型号都不在话下，类似原则大量的汉字被简化其中的一批简化字还可以当作其它汉字的偏旁由此就得到了更多的偏旁类推简化字汉字是一种象形文字，那么为什么中国人会自带繁简转换器呢财之道在知识的海洋里狗刨，这个过程重复多次之后老师没教过的繁体字也就逐渐认识英语感慨文化产品的强是你从小接触繁体字的次数可能远远超出自己的想象一至于你可能没有意识到有多少大陆群众喜闻乐见的文化产品，3301，'
w3 = '重点指出为了构建普适性的且可理解的智能生长机制，需要颠覆传统科学的科学观和方法论对人工智能研究的统领地位，确立信息科学的科学观和方法论对人工智能研究的统领。探究了人工智能理论的核心问题：智能是怎样生成的？结果表明，普适性的智能生成机制乃是“信息转换与智能创生”定律。'
w4 = '基于数字信号处理技术的光纤传感器故障辨识,传统光纤传感器故障辨识方法难以反映光纤传感器故障类型的变化特点,导致光纤传感器故障辨识成功率低,光纤传感器故障辨识错误率高,故障辨识耗时长,为了解决传统光纤传感器故障辨识中存在的难题,设计了基于数字信号处理技术的光纤传感器故障辨识模型。首先分析引起光纤传感器故障误识率高的原因,采用数字信号处理技术采集光纤传感器工作状态信号,从中提取光纤传感器故障特征向量,然后将光纤传感器故障特征向量和故障类型分别作为输入和输出,通过数据挖掘技术设计最优的光纤传感器故障辨识的分类器,最后在Matlab 2017平台上进行了光纤传感器故障辨识仿真模拟测试,结果表明,本文模型可以高精度采集光纤传感器故障信号,能够对全部类型的光纤传感器故障正确辨识,提升了光纤传感器故障辨识成功率,有效减少了光纤传感器故障误识率和识别时间,具有一定实际应用价值。 '
w5 = '一种基于深度学习的遥感图像分类及农田识别方法,为解决便于发现我国基本农田被非法侵占的问题,针对现有神经网络收敛速度慢、识别准确率不高的缺点,提出一种基于卷积神经网络的遥感图像农田分类及识别方法。该算法使用较大的卷积核,有效地提取梯度信息;设计深度为6层的卷积神经网络,提高了网络的分类效果,且大大降低了网络的训练次数。实验结果表明,利用该识别模型对农田、建筑、荒漠以及植被的识别准确率达到98.15%,比经典AlexNet网络模型提高了6.1%;训练网络所需的迭代次数由1.49×106次左右降低到4 500次。因此,与经典AlexNet网络相比,改进的AlexNet网络用于遥感图像分类和目标图像识别,耗时更短、识别准确率更高。 '
w6 = '基于 8􏳷0和深度学习的大数据 指纹识别系统设计􏳣,针对传统指纹识别系统在面对大数据指纹图像时具有识别效率不高􏳦需要手动设计提取的特征的缺点􏳥提出了一 种基于 8􏳷0和深度学习的大数据指纹识别系统􏳪首先􏳥描述了指纹识别系统的原理图􏳪然后􏳥设计了系统硬件框图􏳥采用 +􏳣:􏳦􏳤􏳥􏳧:作为微处理器􏳥采用 􏳶6+􏳦􏳧􏳧 指纹图像作为传感器􏳥并设计了两者之间的接口电路􏳧最后􏳥重点设计了指纹识别的 软件过程􏳥建立一个可以进行指纹自动识别的通用多层深层神经网络􏳪通过设计系统软硬件并进行测试􏳥结果表明文中设 计的指纹识别系统具有很高的指纹识别准确度􏳥能有效处理大数据指纹图像的识别􏳥且与其他基于人工提取特征的方法相 比􏳥具有更高的识别正确率和识别效率􏳪'
w7 = '阿图尔·叔本华（德语：Arthur Schopenhauer，1788年2月22日－1860年9月21日），著名德国哲学家，唯意志论主义的开创者，其思想对近代的学术界、文化界影响极为深远。不同于同时代的费希特、谢林、黑格尔，叔本华并无取消物自体，他继承了康德对物自体和表象之间的区分，认为它是可以透过直观而被认识的，并且将其确定为意志。叔本华认为，意志是独立于时间和空间的，它同时亦包括所有的理性与知识，我们只能透过沉思来摆脱它。叔本华把他著名的悲观主义哲学与此学说联系在一起，认为被意志所支配最终只会带来虚无和痛苦。他对心灵屈从于器官、欲望和冲动的压抑、扭曲的理解启发了日后的精神分析学和心理学。'
w8 = '深度学习（英语：deep learning）是机器学习的分支，是一种以人工神经网络为架构，对数据进行表征学习的算法。[1][2][3][4][5]深度学习是机器学习中一种基于对数据进行表征学习的算法。观测值（例如一幅图像）可以使用多种方式来表示，如每个像素强度值的向量，或者更抽象地表示成一系列边、特定形状的区域等。而使用某些特定的表示方法更容易从实例中学习任务（例如，人脸识别或面部表情识别[6]）。深度学习的好处是用非监督式或半监督式的特征学习和分层特征提取高效算法来替代手工获取特征。[7]表征学习的目标是寻求更好的表示方法并创建更好的模型来从大规模未标记数据中学习这些表示方法。表示方法来自神经科学，并松散地创建在类似神经系统中的信息处理和对通信模式的理解上，如神经编码，试图定义拉动神经元的反应之间的关系以及大脑中的神经元的电活动之间的关系。[8]至今已有数种深度学习框架，如深度神经网络、卷积神经网络和深度置信网络和递归神经网络已被应用在计算机视觉、语音识别、自然语言处理、音频识别与生物信息学等领域并获取了极好的效果。另外，“深度学习”已成为类似术语，或者说是神经网络的品牌重塑'

# 定义选取的词性(名词、专有名词、机构团体、地名、英文单词)
pos = ['n', 'nz', 'nt', 'ns', 'eng', 'nrt', 'l']
stop_key = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]
seg = jieba.posseg.cut(w7)  # 分词
words = []
for i in seg:
    if i.word not in words and i.word not in stop_key and i.flag in pos:  #去重 + 去停用词 + 词性筛选
        words.append(i.word)
x = pd.Series(keywords(words))

# 输出最重要的前10个词
print(x[0:10])
keys = [x[0:10][i][0] for i in range(10)]
result = " ".join(keys)
print(result)
