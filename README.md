# Inteligencia artificial — ejercicios y experimentos

Nueva elaboración de los problemas del repositorio de referencia `Inteligencia_artificial`. Las explicaciones, programas e imágenes se han preparado de nuevo. Los datos Iris y el clasificador Haar son recursos comunes. Las dos imágenes previas de `Unidad 1/Evaluacion` se conservan como antecedentes.

| Tema | Material |
|---|---|
| Reinas, Josephus, cruces, laberinto e islas | [Ejercicios](ejercicios/README.md) |
| A* | [Ruta y costos](evaluacion_a_aterisco/README.md) |
| Iris | [Análisis](dataset_excel/README.md) |
| Perceptrón y XOR | [Experimento en C](percep_modificado/README.md) |
| Dino | [Diseño de datos](reporte_dino_crash_eda/README.md) |
| Árbol y MLP | [Comparación](arbol_red_diferencias/README.md) |
| Preguntas | [Respuestas](preguntas_arboles_nodos_multicapa/README.md) |
| Pelotas | [Dataset](dataset_pelotas_rebotantes/README.md) |
| Convolución | [Cálculo](kernel_convolucion/README.md) |
| Juego | [Órbita de cobre](juego_modificado_arbol/README.md) |
| Haar | [Captura](haarcascade_dataset/README.md) |
| Eigenfaces | [Entrenamiento](entrenar_eigenfaces/README.md) |
| Reconocedores | [Comparación](eigenfaces_fisherfaces_LBPH/README.md) |

Crear un entorno virtual e instalar `requirements.txt`. Ejecutar `python verificacion/comprobar.py` para las comprobaciones numéricas y `python juego_modificado_arbol/juego_pygame_mlp2.py` para el juego.

[VERIFICACION.md](VERIFICACION.md) documenta correcciones y límites. Los prompts se guardan en `verificacion/imagenes.json`. Las imágenes generadas son material didáctico, no evidencia de experimentos o fechas anteriores.

## Inicio en Windows

Desde esta carpeta, el entorno local ya preparado permite iniciar el juego con:

```powershell
.\.venv\Scripts\python.exe juego_modificado_arbol/juego_pygame_mlp2.py
```

En otro equipo: crear el entorno con `python -m venv .venv` e instalar con `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
