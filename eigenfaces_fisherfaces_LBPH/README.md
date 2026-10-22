# Tres representaciones para reconocer rostros

| Método | Representación | Qué observar |
|---|---|---|
| Eigenfaces | Proyección PCA que conserva variación | Sensibilidad a pose e iluminación |
| Fisherfaces | Proyección discriminante que utiliza las identidades | Necesita varias clases y suficientes muestras |
| LBPH | Histogramas de patrones binarios locales | Textura local y configuración de vecindarios |

Las tres alternativas reciben los mismos recortes normalizados. Entrenar produce un modelo XML y un JSON de nombres; **guardar un archivo no mide reconocimiento**. Fuente técnica: [tutorial de OpenCV](https://docs.opencv.org/4.12.0/da/d60/tutorial_face_main.html).

## Uso
`python eigenfaces_fisherfaces_LBPH/eigenfaces.py dataset --salida modelos/eigenfaces.xml`.
Sustituir el ejecutable por `fisherfaces.py` o `lbph.py` y cambiar la salida.

El dataset necesita una carpeta por identidad. Se rechazan conjuntos vacíos y configuraciones insuficientes de Fisherfaces. Para evitar perder resultados, no se sobrescribe una salida existente.

## Comparación experimental pendiente
Reservar imágenes de sesiones distintas, mantener idéntico preprocesamiento y medir matriz de confusión, acierto por identidad y tiempo. Los valores de distancia/confianza de métodos diferentes no son porcentajes comparables. No se inventan resultados sobre rostros: el repositorio no contiene ese dataset. La prueba sintética solo verifica carga, entrenamiento y escritura.
