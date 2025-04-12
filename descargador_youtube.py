import os
from tkinter import *
from tkinter import filedialog, messagebox
from pytube import YouTube
import threading

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_var.set(carpeta)

def iniciar_descarga():
    url = url_var.get().strip()
    carpeta = carpeta_var.get().strip()
    formato = formato_var.get().strip()

    if not url or not carpeta:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    descargar_btn.config(state=DISABLED)
    estado_var.set("Descargando...")
    threading.Thread(target=lambda: descargar_video(url, carpeta, formato)).start()

def descargar_video(url, carpeta, formato):
    try:
        yt = YouTube(url)

        if formato == "MP4":
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=carpeta)
            mensaje = "Video descargado correctamente."
        elif formato == "MP3":
            stream = yt.streams.filter(only_audio=True).first()
            archivo = stream.download(output_path=carpeta)
            base, ext = os.path.splitext(archivo)
            nuevo = base + ".mp3"
            os.rename(archivo, nuevo)
            mensaje = "Audio descargado como MP3 correctamente."
        else:
            mensaje = "Formato no válido."

        estado_var.set("Completado ✅")
        messagebox.showinfo("Éxito", mensaje)

    except Exception as e:
        estado_var.set("Error ❌")
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
    finally:
        descargar_btn.config(state=NORMAL)

# Interfaz Gráfica
ventana = Tk()
ventana.title("Descargador de YouTube MP3/MP4")
ventana.geometry("500x320")
ventana.resizable(False, False)

url_var = StringVar()
carpeta_var = StringVar()
formato_var = StringVar(value="MP4")
estado_var = StringVar(value="Esperando enlace...")

Label(ventana, text="Enlace de YouTube:", font=("Arial", 12)).pack(pady=10)
Entry(ventana, textvariable=url_var, width=55).pack()

Label(ventana, text="Seleccionar formato:", font=("Arial", 12)).pack(pady=10)
frame_formatos = Frame(ventana)
frame_formatos.pack()
Radiobutton(frame_formatos, text="MP4 (Video)", variable=formato_var, value="MP4").pack(side=LEFT, padx=10)
Radiobutton(frame_formatos, text="MP3 (Audio)", variable=formato_var, value="MP3").pack(side=LEFT, padx=10)

Button(ventana, text="Elegir carpeta", command=elegir_carpeta).pack(pady=10)
Label(ventana, textvariable=carpeta_var, fg="blue", wraplength=400).pack()

descargar_btn = Button(ventana, text="Descargar", command=iniciar_descarga, bg="green", fg="white", font=("Arial", 12))
descargar_btn.pack(pady=20)

Label(ventana, textvariable=estado_var, font=("Arial", 10)).pack()

ventana.mainloop()
