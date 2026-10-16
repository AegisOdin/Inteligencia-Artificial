# Inteligencia artificial — ejercicios y experimentos

Nueva elaboración de los problemas del repositorio de referencia `Inteligencia_artificial`. Las explicaciones, programas e imágenes se han preparado de nuevo. Los datos Iris y el clasificador Haar son recursos comunes. Las dos imágenes previas de `Unidad 1/Evaluacion` se conservan como antecedentes.

| Tema | Material |
|---|---|
| Reinas, Josephus, cruces, laberinto e islas | [Ejercicios](ejercicios/README.md) |
| A* | [Ruta y costos](busqueda_ruta_astar/README.md) |
| Iris | [Análisis](exploracion_iris/README.md) |
| Perceptrón y XOR | [Experimento en C](red_xor/README.md) |
| Dino | [Diseño de datos](analisis_dino/README.md) |
| Árbol y MLP | [Comparación](comparativa_clasificadores/README.md) |
| Preguntas | [Respuestas](casos_aprendizaje/README.md) |
| Pelotas | [Dataset](trayectorias_pelotas/README.md) |
| Convolución | [Cálculo](filtros_matriciales/README.md) |
| Juego | [Órbita de cobre](orbita_de_cobre/README.md) |
| Haar | [Captura](captura_rostros/README.md) |
| Eigenfaces | [Entrenamiento](modelo_eigenfaces/README.md) |
| Reconocedores | [Comparación](comparacion_rostros/README.md) |

Crear un entorno virtual e instalar `requirements.txt`. Ejecutar `python verificacion/comprobar.py` para las comprobaciones numéricas y `python orbita_de_cobre/juego_pygame_mlp2.py` para el juego.

[VERIFICACION.md](VERIFICACION.md) documenta correcciones y límites. Los prompts se guardan en `verificacion/imagenes.json`. Las imágenes generadas son material didáctico, no evidencia de experimentos o fechas anteriores.

## Inicio en Windows

Desde esta carpeta, el entorno local ya preparado permite iniciar el juego con:

```powershell
.\.venv\Scripts\python.exe orbita_de_cobre/juego_pygame_mlp2.py
```

En otro equipo: crear el entorno con `python -m venv .venv` e instalar con `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
