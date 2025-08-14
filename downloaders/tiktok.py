import yt_dlp
import os
import uuid

def download(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join(output_dir, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path, filename
