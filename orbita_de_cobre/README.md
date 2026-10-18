# Órbita de cobre

Un robot salta sobre proyectiles y un árbol de decisión aprende sus órdenes manuales. Conserva el problema del juego de referencia: velocidad y distancia como entradas; saltar o esperar como salida, cuatro fotogramas, fondo móvil, nave y colisiones rectangulares.

Ejecutar `python orbita_de_cobre/juego_pygame_mlp2.py` después de instalar las dependencias. M inicia sesión manual nueva y borra datos/modelo; espacio salta; P pausa; T entrena; A juega automáticamente; C exporta CSV; 2/3 muestran gráficas; F cambia pantalla; Q sale. El nombre del archivo se conserva para encontrarlo fácilmente, pero el modelo es un **árbol**, no una MLP.

## Cambios que importan
La etiqueta registra la orden al despegar, no todos los fotogramas en el aire. Solo se toman decisiones desde el suelo. Las rondas se separan entre entrenamiento y prueba para reducir filtración temporal. Se requieren 80 decisiones, tres rondas y ambas acciones; esos mínimos permiten ejecutar, no garantizan un modelo útil. El árbol tiene profundidad máxima 5.

El escenario mantiene 1080×720 como espacio de física incluso al usar pantalla completa; cambiar de pantalla no modifica colisiones. Velocidad y salto usan fotogramas a 45 Hz, como la referencia.

## Recursos
Se regeneran los siete recursos activos y los once visuales de reserva, además de dos sonidos sintetizados. Los sonidos y hojas alternativas se conservan como recursos disponibles; no se presentan como usados por el bucle actual. `fondo.jpg` pasa a `horizonte_alternativo.png`; `jump.mp3` pasa a `impulso.wav`. Los PNG preservan transparencia donde corresponde. Los recursos originales del compañero no se copian.

El fondo se encuadra al cargarlo para alinear la plataforma con los pies. Las ilustraciones no cambian las cajas de colisión. La prueba automática carga las imágenes, recorre frames y entrena con datos sintéticos claramente identificados; esto no sustituye medir supervivencia con partidas humanas.
