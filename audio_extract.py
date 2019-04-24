from pathlib import Path
import os
import subprocess
import shutil


def audio_extract(in_video):
    out_file_mp3 = "./speech-vad-demo/mp3/my_video.mp3"
    file = Path(out_file_mp3)
    if file.exists():
        os.remove(out_file_mp3)
    command_extract = "ffmpeg -i " + in_video + " -f mp3 -vn speech-vad-demo/mp3/my_video.mp3"
    subprocess.call(command_extract, shell=True)

    shutil.rmtree('speech-vad-demo/output_mp3')
    os.mkdir('speech-vad-demo/output_mp3')
    command_split = "ffmpeg -i speech-vad-demo/mp3/my_video.mp3 -f segment -segment_time 10 -c copy " \
                    "speech-vad-demo/output_mp3/my_video%02d.mp3"
    subprocess.call(command_split, shell=True)

    shutil.rmtree('speech-vad-demo/output_pcm')
    os.mkdir('speech-vad-demo/output_pcm')
    dirs = os.listdir('speech-vad-demo/output_mp3')
    for _dir in dirs:
        command_transform = "ffmpeg -y  -i speech-vad-demo/output_mp3/" + _dir \
                            + " -acodec pcm_s16le -f s16le -ac 1 -ar 16000 speech-vad-demo/output_pcm/" + _dir + ".pcm"
        subprocess.call(command_transform, shell=True)



