import threading
import pyautogui
import numpy as np
import sounddevice as sd
import soundfile as sf
from queue import Queue

# Configuración de parámetros de grabación
SCREEN_SIZE = (1920, 1080)  # Tamaño de la pantalla
OUTPUT_FILE = 'grabacion.mp4'  # Archivo de salida
SAMPLE_RATE = 44100  # Tasa de muestreo de audio
FPS = 30

# Variables de control
recording = False
frames = []
audio_frames = Queue()

def record_screen():
    global recording, frames
    frames = []
    while recording:
        img = pyautogui.screenshot()
        frames.append(img)

def record_audio(indata, frames, time, status):
    audio_frames.put(indata.copy())

def start_recording():
    global recording
    recording = True
    t = threading.Thread(target=record_screen)
    t.start()
    stream = sd.InputStream(callback=record_audio, channels=1, samplerate=SAMPLE_RATE)
    stream.start()

def stop_recording():
    global recording
    recording = False
    sd.stop()

def save_video():
    global frames
    frames[0].save(OUTPUT_FILE, save_all=True, append_images=frames[1:], duration=1/FPS, loop=0)

def save_audio():
    audio_data = []
    while not audio_frames.empty():
        audio_data.append(audio_frames.get())
    audio_data = np.concatenate(audio_data, axis=0)
    sf.write(OUTPUT_FILE, audio_data, SAMPLE_RATE)

def main():
    print("Presiona 'Iniciar' para comenzar la grabación.")
    input("Presiona Enter para continuar...")
    start_recording()

    print("Presiona 'Detener' para detener la grabación.")
    input("Presiona Enter para detener la grabación...")
    stop_recording()

    print("Guardando la grabación...")
    save_video()
    save_audio()

    print("Grabación guardada en", OUTPUT_FILE)

if __name__ == '__main__':
    main()
