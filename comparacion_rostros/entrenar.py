import argparse
from contextlib import chdir
from tempfile import TemporaryDirectory
import json
from pathlib import Path
import cv2 as cv
import numpy as np

def cargar(ruta):
    ruta = Path(ruta)
    if not ruta.is_dir():
        raise ValueError(f"No existe el dataset: {ruta}")
    imagenes, etiquetas, nombres = [], [], []
    for carpeta in sorted(p for p in ruta.iterdir() if p.is_dir()):
        leidas = []
        for archivo in sorted(carpeta.iterdir()):
            if archivo.suffix.lower() not in {".png",".jpg",".jpeg",".bmp"}:
                continue
            # imdecode admite rutas Unicode en Windows.
            try:
                contenido = np.fromfile(str(archivo),dtype=np.uint8)
                img = cv.imdecode(contenido,cv.IMREAD_GRAYSCALE) if contenido.size else None
            except cv.error:
                continue
            if img is not None:
                leidas.append(cv.resize(img,(100,100)))
        if not leidas:
            continue
        etiqueta = len(nombres)
        nombres.append(carpeta.name)
        imagenes.extend(leidas)
        etiquetas.extend([etiqueta]*len(leidas))
        print(f"{carpeta.name}: {len(leidas)} imágenes, etiqueta {etiqueta}")
    if len(imagenes) < 2:
        raise ValueError("Se necesitan al menos dos imágenes legibles.")
    return imagenes,np.array(etiquetas,dtype=np.int32),nombres

def entrenar(ruta,metodo,salida):
    imagenes,etiquetas,nombres = cargar(ruta)
    if metodo == "fisherfaces" and (len(nombres) < 2 or len(imagenes) <= len(nombres)):
        raise ValueError("Fisherfaces requiere varias identidades y más imágenes que clases.")
    if not hasattr(cv,"face"):
        raise RuntimeError("Instala opencv-contrib-python para disponer de cv.face")
    fabrica = {"eigenfaces":cv.face.EigenFaceRecognizer_create,
               "fisherfaces":cv.face.FisherFaceRecognizer_create,
               "lbph":cv.face.LBPHFaceRecognizer_create}
    modelo = fabrica[metodo]()
    modelo.train(imagenes,etiquetas)
    salida = Path(salida).resolve()
    salida.parent.mkdir(parents=True,exist_ok=True)
    if salida.exists() or salida.with_suffix(".json").exists():
        raise FileExistsError(f"Elige otra salida para no sobrescribir: {salida}")
    # OpenCV no maneja rutas Unicode de Windows; Python guarda el resultado final.
    with TemporaryDirectory(dir=salida.parent) as temporal:
        with chdir(temporal):
            modelo.write("modelo.xml")
        contenido = (Path(temporal)/"modelo.xml").read_bytes()
        with salida.open("xb") as archivo:
            archivo.write(contenido)
    salida.with_suffix(".json").write_text(json.dumps(nombres,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Modelo guardado: {salida}. Entrenar no mide precisión.")
    return modelo

def main(metodo):
    parser = argparse.ArgumentParser(description=f"Entrenar {metodo} con una carpeta por identidad")
    parser.add_argument("dataset",type=Path)
    parser.add_argument("--salida",type=Path,default=Path("modelos")/f"{metodo}.xml")
    args = parser.parse_args()
    try:
        entrenar(args.dataset,metodo,args.salida)
    except (ValueError,RuntimeError,OSError,cv.error) as exc:
        parser.exit(1,f"Error: {exc}\n")
