"""Genera efectos originales, mono PCM 16 bits, sin archivos de audio ajenos."""
import math
import struct
import wave
from pathlib import Path

def guardar(ruta,duracion,inicio,fin):
    frecuencia = 22050
    cantidad = int(duracion*frecuencia)
    fase = 0.0
    muestras = []
    for i in range(cantidad):
        proporcion = i/(cantidad-1)
        fase += 2*math.pi*(inicio+(fin-inicio)*proporcion)/frecuencia
        envolvente = math.sin(math.pi*proporcion)**2
        muestras.append(int(9000*envolvente*math.sin(fase)))
    with wave.open(str(ruta),"wb") as archivo:
        archivo.setparams((1,2,frecuencia,cantidad,"NONE","not compressed"))
        archivo.writeframes(struct.pack("<"+"h"*cantidad,*muestras))
    with wave.open(str(ruta),"rb") as archivo:
        assert archivo.getnframes() == cantidad and archivo.getsampwidth() == 2

if __name__ == "__main__":
    carpeta = Path(__file__).resolve().parents[1]/"orbita_de_cobre/assets/audio"
    carpeta.mkdir(parents=True,exist_ok=True)
    guardar(carpeta/"jump.wav",.18,350,950)
    guardar(carpeta/"game_over.wav",.6,420,90)
    print("OK: dos efectos PCM originales.")
