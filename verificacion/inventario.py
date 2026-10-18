"""Comprueba correspondencia de imágenes, transparencia, enlaces y sintaxis."""
import ast
import hashlib
import json
import re
import wave
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
REFERENCIA = RAIZ.parent/"Inteligencia_artificial"
CARPETAS = {'arbol_red_diferencias': 'comparativa_clasificadores', 'dataset_excel': 'exploracion_iris', 'dataset_pelotas_rebotantes': 'trayectorias_pelotas', 'eigenfaces_fisherfaces_LBPH': 'comparacion_rostros', 'entrenar_eigenfaces': 'modelo_eigenfaces', 'evaluacion_a_aterisco': 'busqueda_ruta_astar', 'haarcascade_dataset': 'captura_rostros', 'juego_modificado_arbol': 'orbita_de_cobre', 'kernel_convolucion': 'filtros_matriciales', 'percep_modificado': 'red_xor', 'preguntas_arboles_nodos_multicapa': 'casos_aprendizaje', 'reporte_dino_crash_eda': 'analisis_dino'}
RECURSOS = {'audio/game_over.wav': 'audio/fin_partida.wav', 'audio/jump.wav': 'audio/impulso.wav', 'game/fondo.png': 'game/plataforma_cobre.png', 'game/fondo2.png': 'game/desierto_observatorio.png', 'game/fondo_alternativo.png': 'game/horizonte_alternativo.png', 'game/menu.png': 'game/portada_orbita.png', 'game/ufo.png': 'game/dron_enemigo.png', 'junks/cannon.png': 'junks/lanzador_cobre.png', 'junks/dude.png': 'junks/robot_secuencia.png', 'junks/dude_1.png': 'junks/robot_pose.png', 'junks/player1.png': 'junks/explorador_secuencia.png', 'sprites/altair.png': 'sprites/explorador_pose.png', 'sprites/altair2.png': 'sprites/explorador_carrera.png', 'sprites/player.png': 'sprites/robot_movimientos.png', 'sprites/player1.png': 'sprites/robot_acciones.png', 'sprites/purple_ball.png': 'sprites/orbe_energia.png', 'sprites/mono_frame_1.png': 'sprites/robot_carrera_1.png', 'sprites/mono_frame_2.png': 'sprites/robot_carrera_2.png', 'sprites/mono_frame_3.png': 'sprites/robot_carrera_3.png', 'sprites/mono_frame_4.png': 'sprites/robot_carrera_4.png'}
registros = []
for origen in sorted(REFERENCIA.rglob("*")):
    if origen.suffix.lower() not in {".png",".jpg",".jpeg"}:
        continue
    relativo = origen.relative_to(REFERENCIA)
    destino = RAIZ/Path(CARPETAS.get(relativo.parts[0], relativo.parts[0]), *relativo.parts[1:]).with_suffix(".png")
    if relativo.as_posix() == "juego_modificado_arbol/assets/game/fondo.jpg":
        destino = RAIZ/"orbita_de_cobre/assets/game/fondo_alternativo.png"
    if destino.is_relative_to(RAIZ/"orbita_de_cobre/assets"):
        recurso = destino.relative_to(RAIZ/"orbita_de_cobre/assets").as_posix()
        destino = RAIZ/"orbita_de_cobre/assets"/RECURSOS.get(recurso,recurso)
    assert destino.is_file(),f"Falta {destino}"
    assert hashlib.sha256(origen.read_bytes()).digest() != hashlib.sha256(destino.read_bytes()).digest(),f"Imagen copiada: {relativo}"
    with Image.open(destino) as imagen:
        imagen.load()
        alfa = imagen.getextrema()[-1] if imagen.mode == "RGBA" else None
        if "sprites" in relativo.parts or "junks" in relativo.parts or relativo.name == "ufo.png":
            assert alfa is not None and alfa[0] == 0 and alfa[1] > 200,f"Transparencia inválida: {destino}"
        registros.append({"original":relativo.as_posix(),"nuevo":destino.relative_to(RAIZ).as_posix(),
                          "dimensiones":imagen.size,"modo":imagen.mode,"alfa":alfa,
                          "sha256":hashlib.sha256(destino.read_bytes()).hexdigest()})
assert len(registros) == 32
for ruta in RAIZ.rglob("*.md"):
    if ".venv" in ruta.parts or ".git" in ruta.parts:
        continue
    for enlace in re.findall(r"\]\(([^)]+)\)",ruta.read_text(encoding="utf-8")):
        if "://" not in enlace and not enlace.startswith("#"):
            assert (ruta.parent/enlace.split("#")[0]).exists(),f"Enlace roto: {ruta}: {enlace}"
for ruta in RAIZ.rglob("*.py"):
    if ".venv" not in ruta.parts:
        ast.parse(ruta.read_text(encoding="utf-8"),filename=str(ruta))
for nombre in ("impulso.wav","fin_partida.wav"):
    with wave.open(str(RAIZ/"orbita_de_cobre/assets/audio"/nombre)) as sonido:
        assert sonido.getnchannels() == 1 and sonido.getsampwidth() == 2 and sonido.getnframes() > 0
(RAIZ/"verificacion/inventario.json").write_text(json.dumps(registros,indent=2,ensure_ascii=False),encoding="utf-8")
print(f"OK: {len(registros)} imágenes nuevas, transparencias, dos sonidos, enlaces y sintaxis.")
