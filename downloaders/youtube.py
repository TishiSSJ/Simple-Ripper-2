import yt_dlp
import os
import base64
import re

cookies_base64 = os.getenv("COOKIES_TXT_BASE64")
if cookies_base64:
    with open("cookies.txt", "wb") as f:
        f.write(base64.b64decode(cookies_base64))
else:
    print("⚠️ No se encontró COOKIES_TXT_BASE64")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download(url):
    info_opts = {
        'quiet': True,
        'cookiefile': 'cookies.txt',
    }
    # Obtener info primero
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get('title', 'audio'))
    
    output_path = f"/tmp/{title}.%(ext)s"

    ydl_opts_primary = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_primary) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"⚠ Error con M4A: {e}, usando formato alternativo...")
        ydl_opts_fallback = ydl_opts_primary.copy()
        ydl_opts_fallback['format'] = 'bestaudio'
        with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl:
            ydl.download([url])

    mp3_path = f"/tmp/{title}.mp3"
    return mp3_path, f"{title}.mp3"


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

    # Encontrar archivo descargado
    for ext in ['.mp4', '.mkv', '.webm']:
        possible_path = output_path.replace(".%(ext)s", ext)
        if os.path.exists(possible_path):
            return possible_path, os.path.basename(possible_path)

    raise Exception("No se pudo encontrar el archivo descargado")
