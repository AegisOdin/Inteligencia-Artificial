import argparse
from contextlib import chdir
from tempfile import TemporaryDirectory
from pathlib import Path
from uuid import uuid4
import cv2 as cv

def cargar_detector():
    contenido = (Path(cv.data.haarcascades)/"haarcascade_frontalface_alt.xml").read_bytes()
    # La ruta de instalaci?n puede contener acentos que OpenCV no admite.
    with TemporaryDirectory() as temporal:
        (Path(temporal)/"cascade.xml").write_bytes(contenido)
        with chdir(temporal):
            detector = cv.CascadeClassifier("cascade.xml")
    if detector.empty():
        raise RuntimeError("No se pudo cargar Haar.")
    return detector

def capturar(destino,camara=0):
    destino = Path(destino)
    destino.mkdir(parents=True,exist_ok=True)
    detector = cargar_detector()
    captura = cv.VideoCapture(camara)
    try:
        if not captura.isOpened():
            raise RuntimeError("No se pudo abrir la cámara.")
        sesion = uuid4().hex[:12]
        total = 0
        while True:
            ok,frame = captura.read()
            if not ok:
                raise RuntimeError("La cámara dejó de entregar imágenes.")
            gris = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            caras = detector.detectMultiScale(gris,1.3,5)
            vista = frame.copy()
            for x,y,w,h in caras:
                cv.rectangle(vista,(x,y),(x+w,y+h),(40,190,210),1)
            cv.imshow("Espacio: guardar rostros | ESC: salir",vista)
            tecla = cv.waitKey(20)&255
            if tecla == 27:
                break
            if tecla == 32:
                for x,y,w,h in caras:
                    rostro = cv.resize(gris[y:y+h,x:x+w],(100,100))
                    correcto,datos = cv.imencode(".png",rostro)
                    if not correcto:
                        raise RuntimeError("No se pudo codificar el recorte.")
                    nombre = destino/f"{sesion}_{total:04d}.png"
                    with nombre.open("xb") as archivo:
                        archivo.write(datos.tobytes())
                    total += 1
        print(f"Guardados {total} recortes en {destino}")
    finally:
        captura.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capturar recortes de una persona con Haar")
    parser.add_argument("destino",type=Path,help="Por ejemplo dataset/persona_01")
    parser.add_argument("--camara",type=int,default=0)
    args = parser.parse_args()
    try:
        capturar(args.destino,args.camara)
    except (RuntimeError,OSError,cv.error) as exc:
        parser.exit(1,f"Error: {exc}\n")
