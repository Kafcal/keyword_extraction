# coding=utf-8
import codecs


stop_key1 = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]
stop_key2 = [w.strip() for w in codecs.open('data/哈工大停用词表.txt', 'r', encoding='utf-8').readlines()]
stop_key3 = [w.strip() for w in codecs.open('data/四川大学机器智能实验室停用词库.txt', 'r', encoding='utf-8').readlines()]
stop_key4 = [w.strip() for w in codecs.open('data/百度停用词表.txt', 'r', encoding='utf-8').readlines()]
stop_key = list(set(stop_key1 + stop_key2 + stop_key3 + stop_key4))


fileObject = open('data/stopWord.txt', 'w', encoding='utf-8')
for ip in stop_key:
    fileObject.write(ip)
    fileObject.write('\n')

fileObject.close()
