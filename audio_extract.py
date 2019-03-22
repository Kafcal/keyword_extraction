from pathlib import Path
import os
import subprocess


def audio_extract(in_video):
    out_file = "./speech-vad-demo/pcm/my_video.pcm"

    # Check if output file exists. If so, delete it.
    file = Path(out_file)
    if file.exists():
        os.remove(out_file)

    # Process video and/or audio.
    # command = "ffmpeg -i " + in_video + " -ab 160k -ac 2 -ar 44100 -vn " + out_file
    command = "ffmpeg -i " + in_video + " -acodec pcm_s16le -f s16le -ac 1 -ar 16000 " + out_file
    subprocess.call(command, shell=True)  # Run terminal command.


