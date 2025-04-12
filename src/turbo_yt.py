import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from yt_dlp import YoutubeDL

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_var.set(carpeta)

def descargar():
    url = url_var.get().strip()
    carpeta = carpeta_var.get().strip()
    formato = formato_var.get()

    if not url or not carpeta:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    estado_var.set("Descargando...")
    turbo_label.config(text="Turbo activado 🚀")
    descargar_btn.config(state=DISABLED)
    progress_bar['value'] = 0
    progreso_var.set("0%")

    salida = os.path.join(carpeta, '%(title)s.%(ext)s')

    def hook(d):
        if d['status'] == 'downloading':
            porcentaje = float(d['_percent_str'].strip().replace('%', ''))
            progress_bar['value'] = porcentaje
            progreso_var.set(f"{int(porcentaje)}%")
        elif d['status'] == 'finished':
            estado_var.set("Procesando...")

    def proceso():
        try:
            opciones = {
                'outtmpl': salida,
                'progress_hooks': [hook],
                'quiet': True,
                'noprogress': True,
                'windowsconsole': False,
                'external_downloader': 'aria2c',
                'external_downloader_args': ['-x', '16', '-k', '1M'],
            }

            if formato == "mp3":
                opciones.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '0',
                    }]
                })
            elif formato == "mp4":
                opciones.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4'
                })

            with YoutubeDL(opciones) as ydl:
                ydl.download([url])

            estado_var.set("Descarga completada ✅")
            progreso_var.set("100%")
            progress_bar['value'] = 100
            messagebox.showinfo("Éxito", "Descarga completada correctamente.")
        except Exception as e:
            estado_var.set("Error ❌")
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
        finally:
            descargar_btn.config(state=NORMAL)
            turbo_label.config(text="")

    threading.Thread(target=proceso).start()

# GUI
ventana = Tk()
ventana.title("Turbo YT - Convertir YouTube MP3/MP4")
ventana.geometry("500x380")
ventana.resizable(False, False)

url_var = StringVar()
carpeta_var = StringVar()
formato_var = StringVar(value="mp3")
estado_var = StringVar(value="Esperando enlace...")
progreso_var = StringVar(value="0%")

Label(ventana, text="Enlace de YouTube:", font=("Arial", 12)).pack(pady=10)
Entry(ventana, textvariable=url_var, width=60).pack()

Label(ventana, text="Seleccionar formato:", font=("Arial", 12)).pack(pady=10)
FrameFormatos = Frame(ventana)
FrameFormatos.pack()
Radiobutton(FrameFormatos, text="MP3 (Audio)", variable=formato_var, value="mp3").pack(side=LEFT, padx=10)
Radiobutton(FrameFormatos, text="MP4 (Video)", variable=formato_var, value="mp4").pack(side=LEFT, padx=10)

Button(ventana, text="Elegir carpeta", command=seleccionar_carpeta).pack(pady=10)
Label(ventana, textvariable=carpeta_var, fg="blue", wraplength=400).pack()

# 🎨 Estilo verde para barra de progreso
style = ttk.Style(ventana)
style.theme_use('default')
style.configure("green.Horizontal.TProgressbar", troughcolor='white', background='limegreen')

# ✅ Barra de progreso real + porcentaje
progress_bar = ttk.Progressbar(ventana, mode='determinate', length=300, style="green.Horizontal.TProgressbar")
progress_bar.pack(pady=5)

Label(ventana, textvariable=progreso_var, font=("Arial", 10)).pack()

# Turbo label y botón
turbo_label = Label(ventana, text="", font=("Arial", 10, "italic"), fg="green")
turbo_label.pack(pady=2)

descargar_btn = Button(ventana, text="Descargar", command=descargar, bg="green", fg="white", font=("Arial", 12))
descargar_btn.pack(pady=10)

Label(ventana, textvariable=estado_var, font=("Arial", 10)).pack()
Label(ventana, text="© Rodrigo Lovaton (Dr. Dev) - 2025", font=("Arial", 9), fg="gray").pack(pady=10)

ventana.mainloop()
