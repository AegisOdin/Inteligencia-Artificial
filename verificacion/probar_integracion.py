"""Pruebas sintéticas: no representan rendimiento sobre jugadores o rostros reales."""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["MPLBACKEND"] = "Agg"
import importlib.util
import tempfile
from pathlib import Path
import numpy as np
import cv2 as cv
import pygame

RAIZ = Path(__file__).resolve().parents[1]

def modulo(nombre,ruta):
    spec = importlib.util.spec_from_file_location(nombre,ruta)
    resultado = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resultado)
    return resultado

juego = modulo("orbita",RAIZ/"orbita_de_cobre/juego_pygame_mlp2.py")
app = juego.Juego()
assert len(app.frames) == 4
assert all(f.get_size() == (35,52) for f in app.frames)
assert all(f.get_flags()&pygame.SRCALPHA for f in app.frames)
app.menu = False
app.avanzar(True)
assert app.datos[-1][2] == 1 and not app.suelo and app.jugador.y < 610
cantidad = len(app.datos)
app.avanzar(False)
assert len(app.datos) == cantidad
for _ in range(40):
    app.avanzar(False)
assert app.suelo
app.bala = app.jugador.copy()
app.velocidad = 0
ronda = app.ronda
app.avanzar(False)
assert app.ronda == ronda+1
muestras = [(float(-8-r%3),float(d),int(90 <= d <= 150),r)
            for r in range(12) for d in range(0,500,10)]
modelo,acierto = juego.entrenar(muestras)
assert modelo.predict([[-9,120],[-9,400]]).tolist() == [1,0]
try:
    juego.entrenar([(-9.,100.,0,1)]*100)
except ValueError:
    pass
else:
    raise AssertionError("Debe rechazar datos sin saltos")
app.reiniciar()
app.dibujar()
pygame.image.save(app.lienzo,str(RAIZ/"verificacion/juego.png"))
app.menu = True
app.dibujar()
pygame.image.save(app.lienzo,str(RAIZ/"verificacion/menu.png"))
pygame.quit()

haar = modulo("haar",RAIZ/"captura_rostros/haarcascade.py")
assert not haar.cargar_detector().empty()

caras = modulo("caras",RAIZ/"comparacion_rostros/entrenar.py")
with tempfile.TemporaryDirectory(dir=RAIZ/"verificacion") as temporal:
    carpeta = Path(temporal)
    datos = carpeta/"dataset"
    rng = np.random.default_rng(42)
    for persona in range(2):
        destino = datos/f"persona_{persona}"
        destino.mkdir(parents=True)
        for n in range(5):
            imagen = rng.integers(0,60,(100,100),dtype=np.uint8)
            if persona:
                imagen[:,40:60] = 200
            else:
                imagen[40:60,:] = 200
            ok,contenido = cv.imencode(".png",imagen)
            assert ok
            contenido.tofile(str(destino/f"{n}.png"))
    (datos/"persona_0"/"vacio.png").write_bytes(b"")
    (datos/"persona_0"/"corrupto.jpg").write_bytes(b"not an image")
    for metodo in ("eigenfaces","fisherfaces","lbph"):
        salida = carpeta/f"{metodo}.xml"
        caras.entrenar(datos,metodo,salida)
        assert salida.stat().st_size > 0 and salida.with_suffix(".json").exists()
        try:
            caras.entrenar(datos,metodo,salida)
        except FileExistsError:
            pass
        else:
            raise AssertionError("No debe sobrescribir un modelo")
    try:
        caras.cargar(carpeta/"no_existe")
    except ValueError:
        pass
    else:
        raise AssertionError("Debe rechazar rutas inexistentes")
print("OK: juego, etiquetas, colisiones, árbol y tres reconocedores con fixtures sintéticos.")
