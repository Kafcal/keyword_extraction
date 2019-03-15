from aip import AipSpeech
from datetime import datetime
import os
import multiprocessing


# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


class AudioToWords:
    APP_ID = '15657858'
    API_KEY = 'hpfsSY5PnhEBSZk3mjbgoSTH'
    SECRET_KEY = 'lceEAytImCR61u6ZpmigtgiZN9smU0xg'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 文件路径
    path = "./speech-vad-demo/output_pcm/"
    dirs = os.listdir(path)

    # 识别结果
    results_text = []

    def audio_to_words(self, filename):
        data = self.client.asr(get_file_content(self.path + filename), 'pcm', 16000, {
            'dev_pid': 1536,
        })
        if data["err_no"] == 0:
            self.results_text.append(data["result"][0])
            return data["result"][0]
        else:
            return str(data["err_no"])


start_time = datetime.now()

cores = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cores)

# 多核并行处理，音频识别
worker = AudioToWords()
results_text = pool.map(worker.audio_to_words, worker.dirs)

print("dirs:"+str(len(worker.dirs)))
print("results_text:"+str(len(results_text)))
print(results_text)

print("cores:", cores)
end_time = datetime.now()
print("Time used:", end_time-start_time)

# 识别结果写入text.txt
with open('text.txt', 'wt', encoding='utf-8') as f:
    for text in results_text:
        f.write(text)
        f.write(",")
