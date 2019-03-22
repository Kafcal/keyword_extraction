import subprocess

# Set the name/path of input audio
in_audio = "./speech-vad-demo/pcm/" \
           "my_video.pcm"

in_audio1 = "./media/fanjianzhuanhua.pcm"

# 播放16kHz 单声道 16bit的xxx.pcm的PCM文件为例
command = "ffplay -ar 16000 -channels 1 -f s16le -i " + in_audio
subprocess.call(command, shell=True)  # Run terminal command.
