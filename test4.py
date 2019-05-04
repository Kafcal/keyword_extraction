# coding=utf-8
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import jieba
import numpy as np

w1 = '10,维克多雨果,维克多·马里·雨果（法语：Victor Marie Hugo，法语：[viktɔʁ maʁi yɡo]，1802年2月26日－1885年5月22日）是一名法国浪漫主义作家。他是法国浪漫主义文学的代表人物和19世纪前期积极浪漫主义文学运动的领袖，法国文学史上卓越的作家。雨果几乎经历了19世纪法国的所有重大事变。一生创作了众多诗歌、小说、剧本、各种散文和文艺评论及政论文章。代表作有《巴黎圣母院》、《九三年》、和《悲惨世界》等。在法国，雨果主要以诗集纪念，如《静观集》和《历代传说》。他创作了4000多幅画，积极参与许多社会运动，如废除死刑。年轻时，雨果倾向保皇主义，但随着时间推移而改变，成为共和主义的积极推动者；他的作品触及时政、社会和艺术潮流。雨果被葬于巴黎先贤祠。他的遗产被各种方式纪念，包括法国钞票上的肖像。'
w2 = '13,计算机视觉,图像处理和机器视觉守所共有的经典问题电视判定一组图像数据中是否包含某个特定的物体图像，这里所指的信息香香农定义的可以用来帮助做一个决定的信息因为感知可以看作是从干，广信闹钟提醒信息所以计算机视觉也可以看作是研究如何使人工系统中图像或，中国运动特征问题通常可以通过机器自动解决但是到目前为止还没有某个单机的方法能够广泛的，的识别比如简单的几何图形识别人脸识别你说话手写文件识别或者车辆识别，梅创建计算机视觉系统这类系统的组成部分包括过程监控事件事件监测，多维数据中感知的科学做一个工程科学计算机视觉中求进与相关理论与模型，各种情况进行判定在任意环境中识别任意物体现有技术也能够也能够很好的解决特定目标，激情学习所以建立图像恢复的一个计算机是，学研究相关的理论和技术地图创建能够从图像或者多维数据中获取信息的人工智能系统，计算机处理成为更适合人员观察过程送给仪器检测的图像作为一门科学学科计算机，价值计算机视觉包含如下一些分支画面重现实践检测目标跟踪目标识别，你觉得一个补充在生物视觉领域中人类和各种动物的视觉都得到了研究从而创建了这些事，3301，卷席筒钢琴信息过程中所使用的物理模型另一方面在计算机视觉中靠软件和硬件实现的，计算机视觉是一门研究如何使机器看的科学更进一步的说就是指用摄像机和计算，一代替人员对目标进行识别跟踪和测量的机器视觉兵进一步做图像处理，红智能系统得到了研究与描述生物视觉与计算机视觉进行的学科间交叉交刘慧彼此都带来了巨大，而且这些识别需要在特定的环境中具有制定的光照背景和目标指导要求，信息组织物质与环境建模交互交感互动一年级数学同样可以被看做是生物'

wordlist_after_jieba = jieba.cut(w2)
text = " ".join(wordlist_after_jieba)
alice_mask = np.array(Image.open("data/alice_mask.png"))

# wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
#                contour_width=3, contour_color='steelblue', font_path='data/Songti.ttc')
#
# # generate word cloud
# wc.generate(text)
#
# # store to file
# wc.to_file("data/alice.png")
#
# # show
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()
#
wc = WordCloud(background_color="white", max_words=2000, mode="RGBA",
               contour_width=3, contour_color='steelblue', font_path='data/Songti.ttc', width=1000, height=1000)

# generate word cloud
wc.generate(text)

# store to file
wc.to_file("data/test.png")

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()


