from aip import AipSpeech
from datetime import datetime
from utils import get_file_content
from audio_extract import audio_extract
import os
import multiprocessing
import subprocess


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


# 音频提取
audio_extract("./speech-vad-demo/media/" + "water.mp4")
# 音频分割
command = "cd speech-vad-demo && sh build_and_run.sh"
subprocess.call(command, shell=True)

start_time = datetime.now()

cores = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cores)

# 多核并行处理，音频识别
worker = AudioToWords()
results_text = pool.map(worker.audio_to_words, worker.get_dirs())

print("dirs:"+str(len(worker.get_dirs())))
print("results_text:"+str(len(results_text)))
print(results_text)

print("cores:", cores)
end_time = datetime.now()
print("Time used:", end_time-start_time)

# 识别结果写入text.txt
with open('text.txt', 'wt', encoding='utf-8') as f:
    for text in results_text:
        f.write(text)
        f.write("，")
