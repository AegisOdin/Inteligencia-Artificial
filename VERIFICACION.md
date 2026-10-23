# Verificación y diferencias respecto a la referencia

## Alcance

Se completó la carpeta con guion a partir de los temas de la carpeta con guion bajo. Se escribieron explicaciones y programas nuevos, y se generaron 32 imágenes con la herramienta integrada de generación de imágenes: 14 didácticas y 18 recursos visuales del juego. Los dos sonidos se sintetizaron con la biblioteca estándar de Python.

Los 7 recursos visuales activos del juego están incluidos, al igual que los 11 guardados como alternativas. Los PNG mantienen transparencias cuando corresponde. Se conserva el número de fotogramas de las hojas alternativas; no se presupone compatibilidad con recortes antiguos en píxeles porque tienen nuevas dimensiones. El juego actual carga y escala las imágenes individuales.

Las imágenes anteriores de `Unidad 1/Evaluacion` se conservan sin modificaciones como antecedentes. El CSV Iris y el XML Haar se conservan como datos/modelo de referencia; no se alteran para simular originalidad. El repositorio del compañero no se modificó.

## Resultados contrastados

| Problema | Resultado |
|---|---|
| Cuatro reinas | Columnas 3,1,4,2, sin ataques |
| Josephus, n=7, inicio=1, cada segundo | Superviviente 7 |
| Misioneros/caníbales | 11 cruces válidos |
| Laberinto 3×8 | 12 movimientos |
| Islas por lados | 5 componentes |
| A* y Dijkstra | Costo óptimo 102 |
| Ruta del apunte | 5,6,7,17,26,35,44,52,60,59; costo 102 |
| Convolución | Matriz completa en `verificacion/resultados.json` |
| XOR entrenado | 00≈0.009346, 01≈0.989284, 10≈0.991210, 11≈0.008372 |
| Iris | 150 filas × 4 columnas; estadísticas calculadas por bloques |

En A* se permiten diagonales junto a esquinas de muros, como requiere la ruta del apunte. El algoritmo puede devolver otra ruta óptima por desempate. No se copian listas abiertas/cerradas inconsistentes.

Convolución: el primer resultado es 118, no 96. Se declara extensión con ceros y saturación a [0,255]. Pelotas: 3×8×8=192 es solo un cruce simplificado de factores, no una muestra mínima suficiente. El perceptrón de una sola neurona no resuelve XOR; se emplea una red 2–2–1 entrenada.

## Código y recursos probados

- `python verificacion/comprobar.py`: aserciones de los problemas y estadísticas de Iris.
- `gcc -Wall -Wextra -pedantic percep_modificado/percep.c -o percep_modificado/percep.exe -lm`: compila sin advertencias; el ejecutable comprueba las cuatro salidas.
- `python verificacion/probar_integracion.py`: carga de los siete gráficos, salto, aterrizaje, colisión, etiquetas de acción, aprendizaje del árbol y render del juego sin ventana.
- La misma prueba entrena y guarda Eigenfaces, Fisherfaces y LBPH con patrones sintéticos, comprueba rechazo de sobrescrituras y tolerancia a archivos vacíos/corruptos, y carga Haar.
- Se corrigieron rutas Unicode para guardar modelos y cargar Haar en Windows.
- `python verificacion/inventario.py`: correspondencia de las 32 imágenes, contenido diferente a la referencia, transparencia, WAV, sintaxis Python y enlaces locales.
- Capturas renderizadas del programa: [juego](verificacion/juego.png) y [menú](verificacion/menu.png).

## Revisión de imágenes

La matriz de índices muestra 3×8 celdas y la coordenada (1,7). La lámina de convolución se cotejó visualmente con los 25 datos de entrada, 9 coeficientes y 25 resultados.

La primera generación del tablero A* dibujó una ruta sobre un muro; se descartó y se regeneró con casillas coloreadas y números visibles. La primera tabla añadió un tablero incompatible; se reemplazó por una tabla aislada. La versión final conserva las diez casillas y sus costos acumulados. También se corrigió un fondo alternativo que colocaba la plataforma arriba en lugar de abajo.

Las láminas de árboles/redes se revisan contra las explicaciones del repositorio. La imagen de Iris es orientativa: no se usa para validar una identificación botánica. Los sprites se verifican visualmente y mediante carga en Pygame; la física depende de rectángulos, no del dibujo.

Los prompts completos, las revisiones y las rutas están en `verificacion/imagenes.json`; el inventario y hashes finales, en `verificacion/inventario.json`.

## Límites

No se abrió la cámara ni se entrenó con rostros reales. Las pruebas sintéticas confirman ejecución, no precisión de reconocimiento. No se ha medido supervivencia del piloto automático con partidas humanas ni se ha probado pantalla completa en una sesión gráfica real. La tipografía y transparencia del juego se inspeccionaron en las capturas renderizadas.

## Historial de Git

El historial de referencia consultado abarca del 3 de septiembre al 21 de octubre de 2026. Git permite asignar fechas de autor y de commit retrospectivas; eso no acredita que el trabajo se realizó entonces ni cambia la fecha de envío a GitHub. A petici?n del propietario, los nuevos commits se organizan por actividad con fechas de autor y de commit asignadas retrospectivamente, a menos de tres d?as de la actividad correspondiente del historial de referencia. Estas fechas no son evidencia de cu?ndo se elaboraron los archivos. La correspondencia se registra en `verificacion/fechas_commits.json`. El commit anterior se conserva.

## Fuentes técnicas

- [OpenCV: reconocimiento facial](https://docs.opencv.org/4.12.0/da/d60/tutorial_face_main.html).
- [scikit-learn: árboles](https://sklearn.org/stable/modules/tree.html).
- [scikit-learn: redes multicapa](https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/neural_networks_supervised.rst).
