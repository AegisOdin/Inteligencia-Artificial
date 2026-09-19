# Dino: tres preguntas, tres datasets

## Colisión en el próximo frame
Una fila describe t; la etiqueta indica si hay choque en t+1. Entradas: separación horizontal, cajas de colisión, velocidad relativa, posición y velocidad vertical, postura y tipo de obstáculo. A 60 Hz, un frame dura aproximadamente 16.67 ms. No introducir la etiqueta futura como característica.

## Puntaje final
Regresión por partida, observada hasta un punto de corte fijo (por ejemplo 10 segundos). Usar puntos y acciones acumulados hasta ese corte. El objetivo es el puntaje al terminar. Incluir el instante de muerte o el puntaje final entre las entradas filtraría la respuesta.

## Próximo obstáculo
Clasificar cactus pequeño, cactus grande o ave, con altura si corresponde. Si el tipo ya está disponible en el estado del juego, no hace falta aprender a recuperarlo. Predecirlo antes de aparecer requiere demostrar dependencia respecto al historial.

## Evaluación
Separar por partidas completas: fotogramas contiguos no deben repartirse entre entrenamiento y prueba. Cubrir velocidades, saltos, agachadas, obstáculos y colisiones; una partida no garantiza cobertura. Medir recobrado de colisión, falsas alarmas, matriz de confusión y error absoluto de puntaje. Elegir tamaño de muestra con curvas de aprendizaje; no se inventan métricas.
