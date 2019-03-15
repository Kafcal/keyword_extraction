from aip import AipSpeech
import os
from datetime import datetime

start_time = datetime.now()

""" 你的 APPID AK SK """
APP_ID = '15657858'
API_KEY = 'hpfsSY5PnhEBSZk3mjbgoSTH'
SECRET_KEY = 'lceEAytImCR61u6ZpmigtgiZN9smU0xg'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 打开文件
path = "./speech-vad-demo/output_pcm"
dirs = os.listdir(path)

results_text = []

# 识别本地文件
for file in dirs:
    data = client.asr(get_file_content('./speech-vad-demo/output_pcm/'+file), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    if data["err_no"] == 0:
        results_text.append(data["result"][0])

print(results_text)

end_time = datetime.now()
print("Time used:", end_time-start_time)