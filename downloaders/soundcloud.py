import subprocess
import os
import uuid
import yt_dlp

def convert_to_320kbps(input_path):
    output_path = input_path.replace(".mp3", "_320.mp3")
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-b:a", "320k",
        "-y", output_path
    ])
    return output_path

def download(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(output_dir, filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    final_path = convert_to_320kbps(output_path)
    return final_path, os.path.basename(final_path)
