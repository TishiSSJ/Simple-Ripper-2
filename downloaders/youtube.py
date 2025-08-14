import yt_dlp
import os
from utils.convert import convert_to_mp3
import os
import base64

# Cargar cookies base64 y guardarlas como cookies.txt
cookies_base64 = os.getenv("COOKIES_TXT_BASE64")
if cookies_base64:
    with open("cookies.txt", "wb") as f:
        f.write(base64.b64decode(cookies_base64))
else:
    print("⚠️ No se encontró COOKIES_TXT_BASE64")

def download(url):
    output_path = "/tmp/youtube_audio.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    mp3_path = output_path.replace(".%(ext)s", ".mp3")
    return mp3_path, os.path.basename(mp3_path)

def download_video(url):
    output_path = "/tmp/youtube_video.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Encontrar el archivo descargado
    ext_list = ['.mp4', '.mkv', '.webm']
    for ext in ext_list:
        possible_path = output_path.replace(".%(ext)s", ext)
        if os.path.exists(possible_path):
            return possible_path, os.path.basename(possible_path)

    raise Exception("No se pudo encontrar el archivo descargado")
