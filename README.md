# 🎵 Turbo YT - Descargador de YouTube MP3/MP4

Aplicación de escritorio para Windows que permite descargar videos o audios de YouTube en formato MP3 o MP4, con soporte para turbo-descarga vía `aria2c`, conversión automática a MP3, barra de progreso animada y sin necesidad de instalar Python.

## 🚀 Características
- Descarga rápida con `aria2c`
- Interfaz gráfica con barra de progreso
- Conversión automática a MP3
- Ejecutable standalone (.exe)
- Instalador profesional con ícono

## 🛠 Requisitos para desarrollo
- Python 3.10+
- `yt-dlp`, `ffmpeg`, `aria2c`
- PyInstaller (para empaquetar)

## 📦 Compilar
```bash
pyinstaller --onefile --noconsole --icon=assets/icono.ico src/turbo_yt.py
