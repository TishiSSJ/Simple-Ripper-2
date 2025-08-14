import yt_dlp
import os
import base64
import subprocess
import sys

# 1️⃣ Auto-actualizar yt-dlp al arrancar
subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"], check=True)

# Cargar cookies base64 y guardarlas como cookies.txt
cookies_base64 = os.getenv("COOKIES_TXT_BASE64")
if cookies_base64:
    with open("cookies.txt", "wb") as f:
        f.write(base64.b64decode(cookies_base64))
else:
    print("⚠️ No se encontró COOKIES_TXT_BASE64")

def download(url):
    output_path = "/tmp/youtube_audio.%(ext)s"
    
    # Opciones de descarga (prioriza M4A y convierte a MP3 320kbps)
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
        print(f"⚠ Error con M4A: {e}, intentando formato alternativo...")
        ydl_opts_fallback = {
            'format': 'bestaudio',
            'outtmpl': output_path,
            'cookiefile': 'cookies.txt',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl:
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
