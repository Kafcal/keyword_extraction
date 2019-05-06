from audio_to_words import speech_recognition
from keyextract_tfidf import tfidf
from keyextract_textrank import textrank
from keyextract_word2vec_bayes import word2vec_bayes
from keyextract_word2vec_cluster import word2vec_cluster
from keyextract_tfidf_textrank import tfidf_textrank

# 语音识别
video_name = "mcx.mov"
video_title = "计算机视觉"
# speech_recognition(video_name, video_title)

# 关键词抽取
tfidf("data/text_data.csv", "result/keys_TFIDF.csv")
textrank("data/text_data.csv", "result/keys_TextRank.csv")
word2vec_bayes("data/text_data.csv", "result/keys_word2vec_bayes.csv")
word2vec_cluster("data/text_data.csv", "result/keys_word2vec_cluster.csv")
tfidf_textrank("data/text_data.csv", "result/keys_tfidf_textrank.csv")


