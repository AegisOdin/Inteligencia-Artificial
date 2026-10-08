# Nueve preguntas de aplicación

## 1. Árbol de decisión
Asigna una clase mediante condiciones aprendidas de ejemplos etiquetados; busca grupos más homogéneos.

## 2. Partes
Raíz: primera condición. Nodo interno: condición posterior. Rama: resultado de una condición. Hoja: clase o distribución estimada.

## 3. Capas
La entrada recibe variables, las ocultas calculan transformaciones y la salida produce la predicción. Sin activaciones no lineales, apilar capas lineales equivale a una sola transformación lineal.

## 4. Pesos y sesgos
Los pesos modulan entradas y el sesgo desplaza la activación. Un peso aislado no equivale necesariamente a importancia global.

## 5. Aprendizaje
El árbol construye divisiones y hojas; la MLP modifica parámetros para reducir una pérdida con gradientes obtenidos mediante retropropagación.

## 6. Fraude
Un árbol pequeño ofrece reglas inspeccionables con monto, hora, ciudad y frecuencia. Una MLP puede captar interacciones, pero necesita escalado y más ajuste. Empezaría con el árbol y exigiría mejoras en una prueba temporal, especialmente recobrado de fraude a una tasa aceptable de falsas alarmas. Excluir variables conocidas solo después de confirmar el fraude.

## 7. Riesgo escolar
Con precisión similar, comparar recobrado, calibración, estabilidad, equidad y explicación. Preferiría un árbol pequeño si conserva esos resultados, para facilitar apoyos revisados por docentes. No convertir una predicción en una sanción automática.

## 8. Priorización hospitalaria
La precisión agregada no basta: evaluar falsos negativos, subgrupos, calibración, validación clínica y supervisión profesional. Es un análisis de selección de modelos, no una regla de atención médica.

## 9. Reparto
Para un pedido concreto se necesita el tiempo real y el umbral de retraso. Para elegir modelo, reservar muchos pedidos futuros y comparar matriz de confusión, calibración y costo de falsas promesas. Un único desacuerdo no demuestra superioridad.
