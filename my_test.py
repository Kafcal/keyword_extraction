import os
path = "./speech-vad-demo/output_pcm"
dirs = os.listdir(path)

# 识别本地文件
for file in dirs:
    print(file)
