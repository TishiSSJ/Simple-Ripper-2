
# Imagen base oficial de Python
FROM python:3.11-slim

# Instala ffmpeg y curl para debugging (opcional)
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Si existe una variable COOKIES_TXT_BASE64, decodificala
RUN bash -c 'if [ -n "$COOKIES_TXT_BASE64" ]; then echo "$COOKIES_TXT_BASE64" | base64 -d > cookies.txt; fi' || true

# Comando para correr el bot
CMD ["python", "bot.py"]
