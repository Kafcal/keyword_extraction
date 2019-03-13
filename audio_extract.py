from pathlib import Path
import os
import subprocess


# Set the name/path of input and output files.
in_video = "/Users/mochuxian/Downloads/media/video1.mp4"
out_file = "/Users/mochuxian/Downloads/media/video1.pcm"

# Check if output file exists. If so, delete it.
file = Path(out_file)
if file.exists():
    os.remove(out_file)

# Process video and/or audio.
# command = "ffmpeg -i " + in_video + " -ab 160k -ac 2 -ar 44100 -vn " + out_file
command = "ffmpeg -i " + in_video + " -acodec pcm_s16le -f s16le -ac 1 -ar 16000 " + out_file
subprocess.call(command, shell=True)  # Run terminal command.
