from audio_to_words import speech_recognition
from keyextract_tfidf import tfidf
from keyextract_textrank import textrank
from keyextract_word2vec_bayes import word2vec_bayes
from keyextract_word2vec_cluster import word2vec_cluster

# 语音识别
video_name = "mcx.mov"
video_title = "计算机视觉"
speech_recognition(video_name, video_title)

# 关键词抽取
tfidf("data/video_data.csv", "result/video_keys_TFIDF.csv")
textrank("data/video_data.csv", "result/video_keys_TextRank.csv")
word2vec_bayes("data/video_data.csv", "result/video_keys_word2vec_bayes.csv")
word2vec_cluster("data/video_data.csv", "result/video_keys_word2vec_cluster.csv")

