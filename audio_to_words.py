from aip import AipSpeech
from datetime import datetime
from utils import get_file_content
from audio_extract import audio_extract
import os
import multiprocessing
import subprocess
import pandas as pd


class AudioToWords:
    APP_ID = '15657858'
    API_KEY = 'hpfsSY5PnhEBSZk3mjbgoSTH'
    SECRET_KEY = 'lceEAytImCR61u6ZpmigtgiZN9smU0xg'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 文件路径
    path = "./speech-vad-demo/output_pcm/"

    # 识别结果
    results_text = []

    def get_dirs(self):
        return os.listdir(self.path)

    def audio_to_words(self, filename):
        data = self.client.asr(get_file_content(self.path + filename), 'pcm', 16000, {
            'dev_pid': 1536,
        })
        if data["err_no"] == 0:
            self.results_text.append(data["result"][0])
            return data["result"][0]
        else:
            return str(data["err_no"])


def speech_recognition(video_name, video_title):
    # 音频提取
    audio_extract("./speech-vad-demo/media/" + video_name)
    # 音频分割
    command = "cd speech-vad-demo && sh build_and_run.sh"
    subprocess.call(command, shell=True)

    start_time = datetime.now()

    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    # 多核并行处理，音频识别
    worker = AudioToWords()
    results_text = pool.map(worker.audio_to_words, worker.get_dirs())

    print("dirs:" + str(len(worker.get_dirs())))
    print("results_text:" + str(len(results_text)))
    print(results_text)

    end_time = datetime.now()
    print("Time used:", end_time - start_time)

    results_text = "，".join(results_text)

    # 识别结果写入video_data.csv
    data_path = 'data/video_data.csv'
    data = pd.read_csv(data_path)

    ids, titles, contents = list(data["id"]), list(data["title"]), list(data["content"])
    data_count = len(ids)
    ids.append(data_count + 1)
    titles.append(video_title)
    contents.append(results_text)

    result = pd.DataFrame({"id": ids, "title": titles, "content": contents}, columns=['id', 'title', 'content'])
    result.to_csv("data/video_data.csv", index=False)


# video_name = "solink.mp4"
# video_title = "SoLink学术助手小程序"
#
# # 音频提取
# audio_extract("./speech-vad-demo/media/" + video_name)
# # 音频分割
# command = "cd speech-vad-demo && sh build_and_run.sh"
# subprocess.call(command, shell=True)
#
# start_time = datetime.now()
#
# cores = multiprocessing.cpu_count()
# pool = multiprocessing.Pool(processes=cores)
#
# # 多核并行处理，音频识别
# worker = AudioToWords()
# results_text = pool.map(worker.audio_to_words, worker.get_dirs())
#
# print("dirs:"+str(len(worker.get_dirs())))
# print("results_text:"+str(len(results_text)))
# print(results_text)
#
# end_time = datetime.now()
# print("Time used:", end_time-start_time)
#
# results_text = "，".join(results_text)
#
# # 识别结果写入video_data.csv
# data_path = 'data/video_data.csv'
# data = pd.read_csv(data_path)
#
# ids, titles, contents = list(data["id"]), list(data["title"]), list(data["content"])
# data_count = len(ids)
# ids.append(data_count+1)
# titles.append(video_title)
# contents.append(results_text)
#
# result = pd.DataFrame({"id": ids, "title": titles, "content": contents}, columns=['id', 'title', 'content'])
# result.to_csv("data/video_data.csv", index=False)
